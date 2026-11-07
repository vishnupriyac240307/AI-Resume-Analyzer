import re
from pathlib import Path

SKILLS = [
    "python", "java", "c++", "c#", "sql", "mysql", "postgresql", "sqlite",
    "html", "css", "javascript", "typescript", "react", "node.js", "flask",
    "django", "fastapi", "machine learning", "deep learning", "nlp",
    "natural language processing", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn", "power bi", "tableau",
    "excel", "data analysis", "data visualization", "statistics",
    "data science", "big data", "hadoop", "spark", "aws", "azure", "gcp",
    "docker", "git", "github", "rest api", "api development", "linux",
    "communication", "teamwork", "problem solving", "project management",
    "data structures", "algorithms", "oop", "software testing"
]

def extract_text(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ValueError("PDF support is unavailable. Install requirements.txt and try again.") from exc
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise ValueError("DOCX support is unavailable. Install requirements.txt and try again.") from exc
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file type.")

def clean_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def find_skills(text):
    normalized = clean_text(text)
    found = []
    for skill in SKILLS:
        # Match whole terms, while allowing punctuation in common technical names.
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(set(found))

def similarity_score(resume_text, job_text):
    """TF-IDF cosine similarity, with a safe fallback if ML dependencies are absent."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(
            [resume_text, job_text]
        )
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        return 0.0

def analyze_resume(resume_text, job_description):
    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))

    text_similarity = similarity_score(resume_text, job_description)
    skill_coverage = len(matched) / max(len(job_skills), 1)
    # Weighted score balances semantic text overlap and explicit skill coverage.
    score = round((0.45 * text_similarity + 0.55 * skill_coverage) * 100, 1)

    suggestions = []
    if missing:
        suggestions.append("If you genuinely have experience with these skills, add specific evidence: " + ", ".join(missing[:8]) + ".")
    if not re.search(r"\b(project|developed|built|created|implemented)\b", resume_text, re.I):
        suggestions.append("Add a Projects section with the problem, tools used, and measurable outcome.")
    if not re.search(r"\b(intern|internship|experience|work experience)\b", resume_text, re.I):
        suggestions.append("Add relevant internship, volunteering, freelance, or practical experience if applicable.")
    if not re.search(r"\b(19|20)\d{2}\b", resume_text):
        suggestions.append("Check that education and experience dates are clearly listed.")
    if not suggestions:
        suggestions.append("Your resume contains several relevant signals. Improve it further with quantified achievements and concise project descriptions.")

    return {
        "score": score,
        "text_similarity": round(text_similarity * 100, 1),
        "skill_coverage": round(skill_coverage * 100, 1),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
        "word_count": len(resume_text.split()),
    }
