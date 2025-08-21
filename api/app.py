# api/app.py
print("🚀 Starting Flask app…")

import os
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Local imports
from parser.extract_text import parse_resume
from parser.skill_frequencies import get_counts, REQUIRED_SKILLS, demand_rank

# --- App setup ---
app = Flask(__name__)
CORS(app)  # allow all origins during development

# Paths (repo_root = parent of /api)
REPO_ROOT = Path(__file__).resolve().parent.parent
UI_DIR = REPO_ROOT / "ui"

@app.route("/", methods=["GET"])
def home():
    """Root endpoint to confirm API is running and list available routes."""
    return jsonify({
        "message": "Welcome to Data Science Navigator API",
        "available_endpoints": {
            "GET /health": "API health check",
            "GET /skills-demand": "Get current in-demand skills with counts",
            "POST /detect-gap": "Get missing skills sorted by market demand",
            "POST /upload-resume": "Upload a resume file and extract skills",
            "GET /ui": "Serve the frontend UI"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint to ensure API is running."""
    return jsonify({"status": "ok"})

# -------- UI (served by Flask to avoid CORS) --------
@app.route("/ui", methods=["GET"])
def serve_ui_index():
    # http://127.0.0.1:5000/ui
    return send_from_directory(UI_DIR, "index.html")

@app.route("/ui/<path:path>", methods=["GET"])
def serve_ui_assets(path):
    # serve JS/CSS/images alongside index.html
    return send_from_directory(UI_DIR, path)

# -------- API: Resume upload / parsing --------
@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    """
    Expects multipart/form-data with key 'resume' containing the file.
    Returns parsed skills list.
    """
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded (form key must be 'resume')."}), 400

    file = request.files["resume"]
    if not file or file.filename.strip() == "":
        return jsonify({"error": "Empty filename or no file content."}), 400

    try:
        skills = parse_resume(file)  # returns a list of skills (lowercased)
        return jsonify({"skills": skills})
    except Exception as e:
        # Surface a friendly error plus a short technical hint in dev
        return jsonify({
            "error": "Failed to parse resume.",
            "detail": str(e)
        }), 500

# -------- API: Skills demand --------
@app.route("/skills-demand", methods=["GET"])
def skills_demand():
    """Returns current in-demand skills with counts (computed lazily)."""
    try:
        counts = get_counts()  # dict: {skill: count}
        return jsonify({"demand": counts})
    except Exception as e:
        return jsonify({"error": "Failed to compute skills demand.", "detail": str(e)}), 500

# -------- API: Gap detection --------
@app.route("/detect-gap", methods=["POST"])
def detect_gap_route():
    """
    Expects JSON: { "skills": ["python", "sql", ...] }
    Returns missing skills sorted by market demand.
    """
    payload = request.get_json(silent=True) or {}
    found = payload.get("skills", [])
    found_lower = {str(s).lower() for s in found}

    try:
        rank = demand_rank()  # dict: {skill: rank/count}; higher = more in-demand
        missing = [s for s in REQUIRED_SKILLS if s not in found_lower]
        missing_sorted = sorted(missing, key=lambda s: rank.get(s, 0), reverse=True)
        return jsonify({"missing_skills": missing_sorted})
    except Exception as e:
        return jsonify({"error": "Failed to detect gaps.", "detail": str(e)}), 500

if __name__ == "__main__":
    # Tip: keep debug=True during development only
    app.run(debug=True, port=5000)
