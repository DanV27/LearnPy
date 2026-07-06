"""
LearnPy — Flask entry point.

Three categories of routes:

  1. Public pages:  /about, /login, /signup
  2. Auth gates:    /  (Learn home), /lesson/<slug>  (static topic page),
                    /logout
  3. JSON API:      /generate  (only AI-backed endpoint — used by the
                                free-form search bar)

Anything tutorial-related that doesn't come from the sidebar is hand-
authored content in `lessons/*.md`. The AI is only invoked when a user
types something into the search and submits it.
"""

import os
import traceback

from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ before any config reads

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from datetime import datetime

from models import db, User, Generation, LessonProgress
from generator import generate_lesson
from topics import TOPICS, get_topic, visible_in_sidebar, get_parent
from lessons import load_lesson
from challenges import get_challenge
from profile_data import calculate_heatmap
from search_index import build_index,search
from cheatsheets import load_cheatsheet, list_cheatsheets, lesson_to_cheatsheet
from diagram_sequences import get_diagram_sequence


# ---------------------------------------------------------------------------
# App + extension setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

# DATABASE_URL is set in .env (Postgres on Neon in production) or as an
# environment variable on the deploy host. Falls back to local SQLite so
# local dev and CI work with no Postgres running.
_default_db = "sqlite:///codegen.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", _default_db)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)

db.init_app(app)
migrate = Migrate(app, db)  # enables `flask db init/migrate/upgrade`

login_manager = LoginManager()
login_manager.init_app(app)
# Unauthenticated visitors who hit a @login_required route get bounced here.
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id: str):
    """Flask-Login calls this on every request to rehydrate the user from
    whatever it stored in the session cookie (the integer user id)."""
    return User.query.get(int(user_id))


# Auto-create tables for local SQLite only. On Postgres the schema is
# managed by Flask-Migrate — run `flask db upgrade` instead.
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
    with app.app_context():
        db.create_all()

build_index()

# ---------------------------------------------------------------------------
# Error handler — keeps JSON clients from receiving an HTML 500 page
# ---------------------------------------------------------------------------

@app.errorhandler(Exception)
def handle_unexpected_error(err):
    """Any unhandled exception in a JSON endpoint returns JSON instead of
    Flask's HTML debug page (which the frontend's `fetch().then(r=>r.json())`
    can't parse). HTTPExceptions (404, 405, etc.) pass through unchanged."""
    if isinstance(err, HTTPException):
        return err

    app.logger.exception("Unhandled error")

    wants_json = request.is_json or "application/json" in (
        request.headers.get("Accept") or ""
    )
    if wants_json:
        return jsonify({"error": f"Server error: {err}"}), 500

    # Browser navigation — let Flask render its normal error page.
    raise err


# ---------------------------------------------------------------------------
# Template context — make the topic catalog available in every template
# so the sidebar can render it without each route passing it explicitly.
# ---------------------------------------------------------------------------

@app.context_processor
def inject_topics():
    # Only the visible (non-hidden) topics show up in the sidebar drawer.
    # Hidden topics (Basics sub-topics) are still routable directly.
    return {"all_topics": visible_in_sidebar()}


@app.context_processor
def inject_cheatsheets():
    """Make the cheat-sheet catalog available to every template, so the
    sidebar drawer can render the "Cheat Sheets" section on every page."""
    return {"all_cheatsheets": list_cheatsheets()}


@app.context_processor
def inject_user_progress():
    """Inject `user_progress` into every template: a {slug: {viewed, completed}}
    dict. Empty for anonymous users so templates can call it unconditionally."""
    if current_user.is_authenticated:
        return {"user_progress": _user_progress_dict(current_user.id)}
    return {"user_progress": {}}


# ---------------------------------------------------------------------------
# Progress tracking helpers
# ---------------------------------------------------------------------------

def _user_progress_dict(user_id: int) -> dict:
    """Return {slug: {'viewed': True, 'completed': bool}} for a user."""
    rows = LessonProgress.query.filter_by(user_id=user_id).all()
    return {
        r.slug: {"viewed": True, "completed": r.completed_at is not None}
        for r in rows
    }


def _mark_viewed(user_id: int, slug: str) -> None:
    """Upsert a LessonProgress row marking this slug as viewed.

    Safe to call on every page load — does nothing if the row already exists.
    Any DB error is swallowed (logged) so a failed write never prevents the
    lesson from rendering.
    """
    try:
        existing = LessonProgress.query.filter_by(user_id=user_id, slug=slug).first()
        if existing is None:
            db.session.add(LessonProgress(user_id=user_id, slug=slug, viewed_at=datetime.utcnow()))
            db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Failed to mark lesson viewed: user=%s slug=%s", user_id, slug)


def _mark_completed(user_id: int, slug: str) -> None:
    """Upsert a LessonProgress row marking this slug's challenge as completed.

    If the row exists with completed_at already set, this is a no-op.
    """
    try:
        existing = LessonProgress.query.filter_by(user_id=user_id, slug=slug).first()
        now = datetime.utcnow()
        if existing is None:
            db.session.add(LessonProgress(user_id=user_id, slug=slug, viewed_at=now, completed_at=now))
        elif existing.completed_at is None:
            existing.completed_at = now
        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Failed to mark challenge completed: user=%s slug=%s", user_id, slug)


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------


@app.route("/")
@login_required
def index():
    """Home page — the free-form search hero + topic-cards grid."""
    return render_template("main.html", active_topic=None)


@app.route("/about")
def about():
    """Public About page. No login required."""
    return render_template("about.html")

@app.route("/profile")
@login_required
def profile():
    """Profile page"""
    heatmap = calculate_heatmap(current_user.id)
    return render_template("profile.html", heatmap=heatmap)

@app.route("/lesson/<slug>")
@login_required
def lesson_page(slug):
    """Render a hand-authored lesson for a canonical topic.

    The lesson body is a static Markdown file in `lessons/`. We load it
    server-side, resolve its related-topics into real URLs, and embed
    the whole thing into the page via Jinja — no API calls, no waiting.

    Unknown slugs (not in `topics.py`, or no matching `.md` file) redirect
    back to the home page.
    """




    topic = get_topic(slug)
    if not topic:
        return redirect(url_for("index"))

    lesson = load_lesson(slug)
    if not lesson:
        # Catalog entry exists but nobody wrote the lesson file yet.
        return redirect(url_for("index"))

    # `related_slugs` is just slug strings from the frontmatter — turn it
    # into the {slug, name, url} dicts the template expects.
    lesson["related_topics"] = _resolve_related(lesson.pop("related_slugs", []))

    # Resolve the topic's `children` slug list (if any) into full topic dicts
    # with their URL attached. This is what powers the sub-topic grid on
    # parent pages like /lesson/basics.
    children_topics = _resolve_children(topic.get("children") or [])

    #gets parent topic for child topic
    parent_topic = get_parent(slug)

    # Follow-up question buttons shown at the bottom of every lesson.
    # Topics can override the defaults by setting their own `followups`.
    followups = topic.get("followups") or _default_followups(topic["name"])

    # Coding challenge for this lesson, if one is defined in challenges_data.py.
    # The template renders an in-browser code editor + Pyodide-powered test
    # runner when this is present.
    challenge = get_challenge(slug)

    # Record that the current user has viewed this lesson. Adds an eyeball
    # icon to the topic on every grid where it appears.
    _mark_viewed(current_user.id, slug)

    # Pre-light the CHALLENGE COMPLETE badge on lesson pages the user has
    # already beaten in a previous session.
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id, slug=slug
    ).first()
    challenge_completed = progress is not None and progress.completed_at is not None



    return render_template(
        "main.html",
        active_topic=topic,
        active_lesson=lesson,
        children_topics=children_topics,
        followups=followups,
        challenge=challenge,
        challenge_completed=challenge_completed,
        parent_topic=parent_topic,
        diagram_sequence=get_diagram_sequence(slug),
    )



@app.route("/api/search/suggest")
@login_required
def api_search_suggest():
    q = request.args.get("q", "")
    return jsonify(search(q))



@app.route("/cheatsheet/<slug>")
@login_required
def cheatsheet_page(slug):
    sheet = load_cheatsheet(slug)
    if not sheet:
        return redirect(url_for("index"))
    return render_template("cheatsheet.html",
                           active_cheatsheet=sheet,
                           slug=slug)



def _resolve_children(slugs):
    """Turn a list of child topic slugs into full topic dicts with URLs.

    Unknown slugs are silently skipped so a typo in a parent's `children`
    list can't break the index page.
    """
    resolved = []
    for s in slugs or []:
        topic = get_topic(s)
        if topic:
            resolved.append({
                "slug": s,
                "name": topic["name"],
                "icon": topic.get("icon", "menu_book"),
                "level": topic.get("level", ""),
                "description": topic.get("description", ""),
                "url": url_for("lesson_page", slug=s),
            })
    return resolved


def _resolve_related(slugs):
    """Turn a list of slug strings into [{slug, name, url}] dicts.

    Unknown slugs are silently skipped so a typo in a lesson's frontmatter
    can't break the page — it just won't render that chip.
    """
    resolved = []
    for s in slugs or []:
        topic = get_topic(s)
        if topic:
            resolved.append({
                "slug": s,
                "name": topic["name"],
                "url": url_for("lesson_page", slug=s),
            })
    return resolved


def _default_followups(topic_name: str):
    """Generic follow-up question buttons shown at the bottom of every lesson.

    Used when a topic doesn't define its own `followups` list. The prompts
    are built from the topic name so Claude knows what we're elaborating on.
    """
    return [
        {
            "label": "Explain more",
            "prompt": f"Explain {topic_name} in more depth with additional examples.",
        },
        {
            "label": "Why do I need this?",
            "prompt": f"Why is understanding {topic_name} important for a Python developer? Give real-world use cases.",
        },
        {
            "label": "Show a real example",
            "prompt": f"Show me a complete, real-world example that uses {topic_name} in Python.",
        },
        {
            "label": "Common pitfalls",
            "prompt": f"What are common mistakes and pitfalls when working with {topic_name} in Python?",
        },
    ]


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign-up page. GET renders the form; POST receives JSON, creates the
    user, logs them in, and returns the redirect URL."""
    if request.method == "POST":
        try:
            data = request.get_json(silent=True) or {}
            username = (data.get("username") or "").strip()
            email = (data.get("email") or "").strip()
            password = data.get("password") or ""

            # Field-level validation
            if not username or not email or not password:
                return jsonify({"error": "All fields required"}), 400
            if len(password) < 6:
                return jsonify({"error": "Password must be at least 6 characters"}), 400

            # Uniqueness checks (also enforced by DB constraints, but failing
            # here gives a friendlier error message)
            if User.query.filter_by(username=username).first():
                return jsonify({"error": "Username already exists"}), 400
            if User.query.filter_by(email=email).first():
                return jsonify({"error": "Email already exists"}), 400

            user = User(username=username, email=email)
            user.set_password(password)  # hashes via pbkdf2:sha256
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return jsonify({"success": True, "redirect": url_for("index")})

        except Exception as e:
            db.session.rollback()
            app.logger.exception("Signup failed")
            return jsonify({"error": f"Server error: {e}"}), 500

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page. GET renders the form; POST authenticates and sets the
    session cookie."""
    if request.method == "POST":
        try:
            data = request.get_json(silent=True) or {}
            username = (data.get("username") or "").strip()
            password = data.get("password") or ""

            user = User.query.filter_by(username=username).first()
            if not user or not user.check_password(password):
                return jsonify({"error": "Invalid username or password"}), 401

            login_user(user)
            return jsonify({"success": True, "redirect": url_for("index")})

        except Exception as e:
            app.logger.exception("Login failed")
            return jsonify({"error": f"Server error: {e}"}), 500

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Clear the session cookie and bounce back to the login page."""
    logout_user()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# AI endpoint — the only place Claude is called from
# ---------------------------------------------------------------------------

@app.route("/generate", methods=["POST"])
@login_required
def generate():
    """Generate a short Python lesson from a free-form search prompt.

    Called by the search bar on the home page. The lesson is also persisted
    to the `Generation` table so we can build a per-user history view later.
    """
    data = request.get_json(silent=True) or {}
    spec = (data.get("prompt") or "").strip()

    if not spec:
        return jsonify({"error": "Prompt is empty."}), 400

    try:
        lesson = generate_lesson(spec)

        # Persist the generation for the user's history. Wrapped in its own
        # try/except because a DB problem here shouldn't block the response —
        # the lesson is still useful even if we couldn't save it.
        try:
            generation = Generation(
                user_id=current_user.id,
                spec=spec[:500],
                title=(lesson.get("title") or spec)[:200],
                lesson_markdown=lesson.get("lesson_markdown") or "",
                code=lesson.get("code") or "",
            )
            db.session.add(generation)
            db.session.commit()
            lesson["generation_id"] = generation.id
        except Exception as save_err:
            db.session.rollback()
            lesson["save_error"] = str(save_err)

        return jsonify(lesson)

    except Exception as e:
        app.logger.exception("Lesson generation failed")
        return (
            jsonify({"error": str(e), "trace": traceback.format_exc()}),
            500,
        )


# ---------------------------------------------------------------------------
# Progress API — called by the challenge runner when all tests pass.
# ---------------------------------------------------------------------------

@app.route("/api/progress/complete", methods=["POST"])
@login_required
def api_progress_complete():
    """Record that the current user passed the challenge for `slug`.

    Idempotent — calling again on an already-completed lesson is a no-op.
    Validates the slug exists in the catalog so the client can't insert
    arbitrary keys into the table.
    """
    data = request.get_json(silent=True) or {}
    slug = (data.get("slug") or "").strip()

    if not slug or get_topic(slug) is None:
        return jsonify({"error": "Unknown slug"}), 400

    _mark_completed(current_user.id, slug)
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# Dev server entry point. In production, run with gunicorn/uwsgi.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
