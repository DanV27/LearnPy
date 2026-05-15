from flask import Flask, render_template, request, jsonify, Response
from generator import (
    generate_code,
    validate_syntax,
    run_test,
    fix_code,
    analyze_complexity,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/generate", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
