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

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.exceptions import HTTPException

from models import db, User, Generation
from generator import generate_lesson
from topics import TOPICS, get_topic
from lessons import load_lesson


# ---------------------------------------------------------------------------
# App + extension setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

# SQLite file lives in Flask's instance folder (`instance/codegen.db`).
# Delete that file if you change the schema in `models.py` — Flask-SQLAlchemy
# won't migrate existing tables for you.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///codegen.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
# Unauthenticated visitors who hit a @login_required route get bounced here.
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id: str):
    """Flask-Login calls this on every request to rehydrate the user from
    whatever it stored in the session cookie (the integer user id)."""
    return User.query.get(int(user_id))


# Create any missing tables on startup. Safe to run repeatedly — it does
# nothing if the tables already exist.
with app.app_context():
    db.create_all()


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
    return {"all_topics": TOPICS}


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

    return render_template(
        "main.html",
        active_topic=topic,
        active_lesson=lesson,
    )


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
# Dev server entry point. In production, run with gunicorn/uwsgi.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
