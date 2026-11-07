from pathlib import Path
from datetime import datetime
import os
import re
import sqlite3
import uuid

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from analyzer import analyze_resume, extract_text

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = BASE_DIR / "resume_analyzer.db"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-for-production")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                role TEXT NOT NULL,
                score REAL NOT NULL,
                matched_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    with db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
        avg = conn.execute("SELECT AVG(score) FROM analyses").fetchone()[0] or 0
        recent = conn.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT 5").fetchall()
    return render_template("index.html", total=total, avg=round(avg, 1), recent=recent)

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        resume = request.files.get("resume")
        role = request.form.get("role", "").strip()
        job_description = request.form.get("job_description", "").strip()

        if not resume or not resume.filename:
            flash("Choose a resume file to continue.", "error")
            return redirect(url_for("analyze"))
        if not allowed_file(resume.filename):
            flash("Unsupported file. Upload a PDF, DOCX, or TXT file.", "error")
            return redirect(url_for("analyze"))
        if not role:
            flash("Enter the target job role.", "error")
            return redirect(url_for("analyze"))
        if not job_description:
            flash("Paste the job description so the match score has context.", "error")
            return redirect(url_for("analyze"))

        safe_name = secure_filename(resume.filename)
        stored_name = f"{uuid.uuid4().hex}_{safe_name}"
        path = UPLOAD_DIR / stored_name
        resume.save(path)
        try:
            resume_text = extract_text(path)
            if len(resume_text.strip()) < 40:
                raise ValueError("Not enough readable text was found. Try a text-based PDF or DOCX.")
            result = analyze_resume(resume_text, job_description)
            with db() as conn:
                cur = conn.execute(
                    """INSERT INTO analyses
                    (filename, role, score, matched_skills, missing_skills, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (safe_name, role, result["score"],
                     ", ".join(result["matched_skills"]),
                     ", ".join(result["missing_skills"]),
                     datetime.now().strftime("%Y-%m-%d %H:%M"))
                )
                analysis_id = cur.lastrowid
            return render_template("result.html", result=result, filename=safe_name,
                                   role=role, analysis_id=analysis_id)
        except Exception as exc:
            flash(str(exc), "error")
            return redirect(url_for("analyze"))
        finally:
            # Uploaded resumes are processed locally and then removed.
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
    return render_template("analyze.html")

@app.route("/history")
def history():
    with db() as conn:
        rows = conn.execute("SELECT * FROM analyses ORDER BY id DESC").fetchall()
    return render_template("history.html", rows=rows)

@app.route("/history/export")
def export_history():
    import csv
    from io import StringIO, BytesIO
    with db() as conn:
        rows = conn.execute("SELECT filename, role, score, matched_skills, missing_skills, created_at FROM analyses ORDER BY id DESC").fetchall()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Resume", "Target role", "Match score", "Matched skills", "Missing skills", "Analyzed at"])
    for row in rows:
        writer.writerow(list(row))
    data = BytesIO(output.getvalue().encode("utf-8-sig"))
    data.seek(0)
    return send_file(data, mimetype="text/csv", as_attachment=True, download_name="resume_analysis_history.csv")

@app.errorhandler(413)
def too_large(_):
    flash("File is too large. Maximum upload size is 8 MB.", "error")
    return redirect(url_for("analyze"))

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)