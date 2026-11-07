# ResumeIQ – AI-Powered Resume Analyzer

An intelligent resume analysis application that evaluates how well a candidate's resume matches a given job description using Machine Learning and Natural Language Processing (NLP) techniques.

ResumeIQ analyzes resume content, calculates a compatibility score, identifies matching and missing skills, and provides actionable suggestions to help candidates improve their resumes.

---

## Project Overview

Finding the right job requires more than just having a resume. Candidates need to understand whether their skills and qualifications align with the requirements of a particular job role.

**ResumeIQ** addresses this challenge by providing an automated resume analysis system that compares uploaded resumes with job descriptions and generates meaningful insights.

The application uses TF-IDF vectorization, cosine similarity, and skill-based analysis to evaluate resume relevance.

## Key Features

- **Resume Upload:** Supports PDF, DOCX, and TXT file formats.
- **Text Extraction:** Extracts relevant content from uploaded resumes.
- **Resume Matching:** Compares resume content with job descriptions using TF-IDF and cosine similarity.
- **Compatibility Score:** Generates an estimated resume matching score.
- **Skill Analysis:** Identifies skills that match the job requirements.
- **Skill Gap Detection:** Highlights skills that were not detected in the resume.
- **Improvement Suggestions:** Provides recommendations to improve resume relevance.
- **Analysis History:** Stores previous analysis summaries using SQLite.
- **CSV Export:** Allows users to download analysis history.
- **Modern Dashboard:** Provides a clean, responsive, and professional user interface.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Machine Learning | Scikit-learn |
| NLP Techniques | TF-IDF, Cosine Similarity |
| Data Processing | Python |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Document Processing | PyPDF, python-docx |
| Data Export | CSV |

## How It Works

1. The user uploads a resume in PDF, DOCX, or TXT format.
2. The system extracts text from the uploaded document.
3. The user enters the target job role and job description.
4. The application preprocesses the resume and job description.
5. TF-IDF vectorization converts the text into numerical representations.
6. Cosine similarity calculates textual similarity.
7. The system identifies matched and missing skills.
8. A weighted compatibility score is generated.
9. The dashboard displays the analysis results and improvement suggestions.

## Resume Matching Methodology

ResumeIQ uses a weighted scoring approach:

**Overall Matching Score =**

- 45% – TF-IDF Text Similarity
- 55% – Job Skill Coverage

The system combines textual similarity and skill coverage to produce an estimated compatibility score.

**Note:** This is an educational matching heuristic, not a validated recruitment assessment or a probability of getting hired.

## Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── analyzer.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── analyze.html
│   ├── result.html
│   └── history.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── uploads/
│   └── .gitkeep
│
└── tests/
    └── test_analyzer.py
```

## Installation and Setup

### Prerequisites

- Python 3.10 or higher
- Git
- VS Code or any Python IDE

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Resume-Analyzer.git
```

### Step 2: Navigate to the Project Folder

```bash
cd AI-Resume-Analyzer
```

### Step 3: Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
py -m venv .venv
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Open in Browser

```text
http://127.0.0.1:5001
```

The ResumeIQ application will now be available locally.

## Running Tests

Execute the following command to run the automated unit tests:

```bash
python -m unittest discover -s tests -v
```

## Sample Use Case

**Target Job Role:** Junior Data Analyst

**Example Required Skills:**
- Python
- SQL
- Excel
- Power BI
- Tableau
- Pandas
- NumPy
- Statistics
- Data Visualization

ResumeIQ compares these requirements against the uploaded resume and identifies detected skills, potential skill gaps, and improvement opportunities.

## Privacy and Limitations

- Uploaded resumes are processed locally by the application.
- Uploaded resume files are deleted after processing.
- Analysis summaries are stored in a local SQLite database.
- Scanned image-only PDFs may not produce extractable text.
- Skill detection depends on a predefined skill vocabulary.
- A missing skill indicates that the system did not detect it; it does not prove the candidate lacks that skill.

This project is intended for educational and portfolio purposes. It should not be used as the sole basis for recruitment decisions.

## Future Enhancements

- Integration with Large Language Models (LLMs).
- Advanced semantic similarity using Sentence Transformers.
- Automatic resume improvement and rewriting.
- ATS keyword optimization.
- Resume ranking for multiple job descriptions.
- User authentication and personalized dashboards.
- Cloud deployment and online accessibility.

## Author

**Vishnu Priya**

B.Sc. Computer Science with Data Analytics

Interested in Artificial Intelligence, Machine Learning, Data Analytics, and Software Development.

---

⭐ If you find this project interesting, consider giving the repository a star!

**Built with Python, Machine Learning, and curiosity.** 💙
