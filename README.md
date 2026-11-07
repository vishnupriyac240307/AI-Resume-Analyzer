# ResumeIQ — AI Resume Analyzer

A local Flask web application that compares a resume with a target job description and produces an explainable match estimate, skill-gap analysis, and improvement suggestions.

## Features

- Upload PDF, DOCX, or TXT resumes (maximum 8 MB).
- Extract text locally from uploaded documents.
- Compare resume and job description using TF-IDF cosine similarity.
- Detect skills from a built-in vocabulary and calculate job-skill coverage.
- Show matched skills, skills not found, and improvement suggestions.
- Save analysis summaries in SQLite and export history to CSV.
- Responsive professional dashboard.
- Uploaded resume files are deleted after processing; the analysis summary is retained locally.

## Important limitations

This is an educational portfolio project, not a validated recruitment product. Its score is a heuristic:
- 45% TF-IDF text similarity
- 55% detected job-skill coverage

The skill vocabulary is intentionally finite. Synonyms, context, skill proficiency, seniority, experience quality, and candidate potential are not reliably assessed. A missing skill means it was not detected in the text; it does not prove the candidate lacks that skill. The score is not a probability of being hired. Do not add skills to a resume unless they are genuinely held.

Scanned/image-only PDFs may not contain extractable text. Use a text-based PDF or DOCX.

## Requirements

- Python 3.10 or newer (Python 3.11 recommended)
- macOS, Windows, or Linux
- Internet connection during initial dependency installation. The app itself runs locally; Google Fonts and Chart.js are optional external UI resources.

## Run on macOS

Open Terminal and navigate to the extracted project folder:

```bash
cd ai_resume_analyzer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

To stop the server, press `Control + C` in Terminal.

## Run on Windows

```powershell
cd ai_resume_analyzer
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**.

## How to use

1. Select **Analyze resume**.
2. Upload a PDF, DOCX, or TXT resume.
3. Enter a target role, for example `Junior Data Analyst`.
4. Paste the complete job description.
5. Select **Analyze resume**.
6. Review the overall estimate, text similarity, skill coverage, matched skills, missing skills, and suggestions.
7. Visit **Analysis history** to review saved summaries or export them to CSV.

## Project structure

```text
ai_resume_analyzer/
├── app.py
├── analyzer.py
├── requirements.txt
├── README.md
├── resume_analyzer.db       # created automatically on first run
├── uploads/                 # temporary upload location
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── analyze.html
│   ├── result.html
│   └── history.html
├── static/
│   ├── css/style.css
│   └── js/app.js
└── tests/
    └── test_analyzer.py
```

## Tests

After installing requirements:

```bash
python -m unittest discover -s tests -v
```

## Privacy and deployment

The application is configured for local demonstration. Uploaded files are removed after processing, but this is not a security audit. Before public deployment, add authentication, CSRF protection, secure secret management, rate limiting, malware scanning, access controls, and production server configuration. Do not upload sensitive personal data to an untrusted deployment.
