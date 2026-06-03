from flask import Flask, Response, render_template, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

from models import db, User, Generation
from generator import (
    generate_code,
    validate_syntax,
    run_test,
    fix_code,
    analyze_complexity,
)

app = Flask(__name__)

#config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codegen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')



# ===== DATABASE & LOGIN =====
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables on startup
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("main.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign up page"""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip()
        password = data.get("password") or ""
        
        # Validation
        if not username or not email or not password:
            return jsonify({"error": "All fields required"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Log them in
        login_user(user)
        return jsonify({"success": True, "redirect": url_for("index")})
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401
        
        login_user(user)
        return jsonify({"success": True, "redirect": url_for("index")})
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for("login"))

@app.route("/generate", methods=["POST"])
@login_required
def generate():
    """Run the full pipeline: generate -> validate -> test -> (optional) fix."""
    data = request.get_json(silent=True) or {}
    spec = (data.get("prompt") or "").strip()

    if not spec:
        return jsonify({"error": "Prompt is empty."}), 400

    try:
        # Step 1: Generate code + tests
        code, test_code = generate_code(spec)
        print(f"[DEBUG] First 200 chars of code:\n{repr(code[:200])}")

        result = {
            "code": code,
            "test_code": test_code,
            "valid_syntax": False,
            "fixed": False,
        }

        # Step 2: Validate syntax
        result["valid_syntax"] = validate_syntax(code)

        if not result["valid_syntax"]:
            return jsonify(result)

        # Step 3: Run tests
        test_result = run_test(code, test_code)
        result["test_result"] = {
            "passed": test_result["passed"],
            "passed_count": test_result["passed_count"],
            "failed_count": test_result["failed_count"],
            "total": test_result["total"],
            "output": test_result["output"][-4000:],  # cap to avoid huge payloads
            "errors": test_result["errors"][-2000:],
        }

        # Step 4: Attempt a fix if tests failed
        if not test_result["passed"]:
            try:
                fixed = fix_code(code, test_code, test_result)
                if validate_syntax(fixed):
                    fixed_result = run_test(fixed, test_code)
                    result["fixed"] = True
                    result["fixed_test_result"] = {
                        "passed": fixed_result["passed"],
                        "passed_count": fixed_result["passed_count"],
                        "failed_count": fixed_result["failed_count"],
                        "total": fixed_result["total"],
                    }
                    if fixed_result["passed"]:
                        # Promote the fix to be the returned code
                        result["code"] = fixed
            except Exception as fix_err:
                result["fix_error"] = str(fix_err)

        # Step 5: Complexity analysis on the final code
        try:
            result["complexity"] = analyze_complexity(result["code"])
        except Exception as ce:
            result["complexity_error"] = str(ce)

        return jsonify(result)

    except Exception as e:
        import traceback

        return (
            jsonify({"error": str(e), "trace": traceback.format_exc()}),
            500,
        )


@app.route("/download", methods=["POST"])
def download():
    """Return generated code as a downloadable .py file."""
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")
    filename = data.get("filename", "generated.py")
    return Response(
        code,
        mimetype="text/x-python",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

@app.route("/history")
@login_required
def history():
    """Get user's generation history"""
    generations = Generation.query.filter_by(user_id=current_user.id).order_by(Generation.created_at.desc()).all()
    return jsonify([g.to_dict() for g in generations])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
