# 🎯 AI Resume Analyzer & Job Matcher

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-TF--IDF%20%26%20Cosine%20Similarity-F7931E.svg)](https://scikit-learn.org/)
[![spaCy & Regex](https://img.shields.io/badge/NLP-spaCy%20%26%20Pattern%20Matching-09A3D5.svg)](https://spacy.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=zakirsameerk6/Resume_Analyser&branch=main&mainModule=app.py)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

An intelligent, privacy-first Python web application that extracts skills from resumes, analyzes alignment against job descriptions, computes skill coverage and TF-IDF text similarity scores, pinpoints missing competencies, and generates curated learning recommendations.

---

## 🌟 Key Features

1. **📄 PDF Resume Parsing**: Automatically extracts and sanitizes text from PDF resumes using high-performance **PyMuPDF (`fitz`)**, handling multi-column layouts, page breaks, and bullet normalization.
2. **🧠 Multi-Layer Skill Extraction**: Identifies 60+ technical and analytical skills (Python, SQL, Excel, Power BI, React, Docker, Machine Learning, AWS, etc.) using boundary-aware regular expressions and NLP tokenization.
3. **🎯 Comprehensive Job Description Matching**:
   - **Skill Coverage Score**: Percentage of required skills found in the candidate's resume.
   - **Text Similarity Score**: Cosine similarity between resume and job description calculated using **TF-IDF vectorization**.
   - **Overall Weighted Alignment**: Configurable composite index balancing hard skill coverage and contextual textual relevance.
4. **⚠️ Gap Identification**: Automatically detects required skills absent from the resume and categorizes extra strengths.
5. **💡 Targeted Learning Pathways**: Recommends official documentation, tutorials, courses, and estimated completion times for each detected skill gap.
6. **📊 Interactive Streamlit Dashboard**: Intuitive, responsive interface with metric cards, color-coded status badges, and domain breakdown charts.
7. **📥 Report Export**: One-click download of a structured **CSV analysis report** (via Pandas) and an **Executive Summary (Markdown)**.
8. **⚡ 1-Click Sample Demos**: Test immediately with preloaded sample resumes and job postings (Data Analyst and Full Stack Engineer).

---

## 🏗️ Architecture & How It Works

```
┌─────────────────┐      ┌──────────────────────────┐
│  Resume (PDF)   │      │  Job Description (Text)  │
└────────┬────────┘      └────────────┬─────────────┘
         │                            │
   [PyMuPDF fitz]                     │
         ▼                            ▼
  Extracted Text            Raw Job Description
         │                            │
         ├────────────────────────────┤
         │                            │
         ▼                            ▼
  [Skill Extractor]          [Skill Extractor]
 (Regex & spaCy NLP)        (Regex & spaCy NLP)
         │                            │
         └─────────────┬──────────────┘
                       │
                       ▼
               [Matching Engine]
   ├── Skill Coverage Score: (Matched / Required) * 100
   ├── Text Similarity: Cosine_Similarity(TF-IDF_Resume, TF-IDF_JD)
   └── Composite Weighted Match Score
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
  [Skill Gap Analysis]     [Recommender Engine]
 (Matched, Missing, Extra) (Curated Docs & Time Estimates)
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
          [Streamlit Interactive Dashboard]
        ├── Metric KPI Cards & Skill Badges
        ├── Domain Category Breakdown Chart
        └── CSV & Markdown Report Downloaders
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+** | Core application logic and algorithmic pipeline |
| **React 18 & Vite** | Modern, responsive frontend SPA with Lucide icons |
| **Tailwind CSS** | Clean, responsive design with color-coded skill badges |
| **FastAPI & Uvicorn** | High-performance asynchronous REST API backend |
| **Streamlit** | Rapid interactive web dashboard and state management |
| **PyMuPDF (`fitz`)** | Fast, robust PDF text extraction and document sanitization |
| **spaCy** | Tokenization, lemmatization, and linguistic NLP processing |
| **Scikit-learn** | TF-IDF Vectorization and Cosine Similarity computations |
| **Regular Expressions (`re`)** | Boundary-accurate skill pattern matching and alias resolution |
| **Pandas** | Tabular data manipulation and CSV report generation |
| **Git & GitHub** | Version control, documentation, and portfolio showcase |

---

## 📂 Project Structure

```
Resume_Analyser/
├── app.py                      # Streamlit interactive web dashboard
├── server.py                   # FastAPI REST API & static server
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Comprehensive project documentation
├── frontend/                   # Modern React + Tailwind CSS SPA
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   ├── dist/                   # Production build assets
│   └── src/
│       ├── App.jsx             # Main interactive React application
│       ├── main.jsx
│       └── index.css
├── src/                        # Core Python intelligence modules
│   ├── __init__.py
│   ├── pdf_extractor.py        # PyMuPDF text extraction & cleanup
│   ├── skill_database.py       # Taxonomy of skills, aliases, and learning resources
│   ├── skill_extractor.py      # Regex & NLP skill detection engine
│   ├── matcher.py              # Skill coverage & TF-IDF similarity algorithms
│   ├── recommender.py          # Learning resource & action plan generator
│   └── report_generator.py     # Pandas DataFrame & CSV exporter
├── sample_data/                # Built-in sample resumes & job descriptions
│   ├── sample_resume_data_analyst.pdf / .txt
│   ├── sample_jd_data_analyst.txt
│   ├── sample_resume_software_engineer.pdf / .txt
│   └── sample_jd_software_engineer.txt
└── tests/                      # Automated unit test suite
    └── test_analyzer.py        # Comprehensive tests for all modules
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create and Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ Choose Your Frontend Experience

### Option A: Modern React + FastAPI Full-Stack App (Recommended)
Launch the FastAPI backend (which also serves the compiled React frontend):
```powershell
.\.venv\Scripts\python.exe server.py
```
Open **`http://localhost:8000`** in your browser!

*For active frontend React development with Hot Module Replacement (HMR):*
```bash
cd frontend
npm run dev
```
Open **`http://localhost:5173`**.

---

### Option B: Streamlit Web Dashboard
Run the standalone Streamlit application:
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Open **`http://localhost:8501`** in your browser!

---

## 🌐 Live Deployment Guide (Get a Free Public URL)

You can deploy this application online for free in under 60 seconds so recruiters and interviewers can use it live:

### 1. Streamlit Community Cloud (Instant 1-Click Deploy - Free Forever)
1. Visit **[share.streamlit.io](https://share.streamlit.io/)** and click **"Continue with GitHub"**.
2. Click **"New app"**.
3. Set:
   - **Repository:** `zakirsameerk6/Resume_Analyser`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy!"**.
5. Streamlit will build your app and give you a free public link:
   👉 **`https://<your-custom-name>.streamlit.app`**

### 2. Render.com (Deploy Full-Stack React + FastAPI - Free)
1. Go to **[render.com](https://render.com/)** and sign in with GitHub.
2. Click **"New +"** -> **"Web Service"** -> select `zakirsameerk6/Resume_Analyser`.
3. Set:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn server:app --host 0.0.0.0 --port $PORT`
4. Click **"Create Web Service"**.
5. Render gives you a public HTTPS URL:
   👉 **`https://resume-analyser-xxx.onrender.com`**

---

## 🧪 Running Unit Tests

Run the test suite to verify extraction, matching, and scoring algorithms:
```bash
python -m unittest tests/test_analyzer.py -v
```

---

## 💡 How Scoring Works

### 1. Skill Coverage Score
Measures the proportion of required competencies found in the resume:
$$\text{Skill Coverage Score} = \left(\frac{|\text{Matched Skills}|}{|\text{Skills Required in Job Description}|}\right) \times 100$$

### 2. Text Similarity Score (TF-IDF & Cosine Similarity)
Transforms the entire resume and job description into n-gram Term Frequency-Inverse Document Frequency vectors:
$$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|} \times 100$$

### 3. Overall Weighted Score
Combines skill coverage and text similarity using adjustable weights (default: 60% skills, 40% text):
$$\text{Overall Score} = (0.60 \times \text{Skill Coverage}) + (0.40 \times \text{Text Similarity})$$

---

## 💼 Interview Talking Points

When presenting this project to interviewers:
1. **Deterministic vs. Generative**: Explain why a rule-based + traditional NLP approach is preferred here: 100% deterministic, zero API cost, instantaneous execution, and strict candidate data privacy (no resume text sent to third-party LLM endpoints).
2. **Boundary-Aware Regex & Aliases**: Discuss how false positives are prevented (e.g., distinguishing `Java` from `JavaScript`, handling `Power BI` vs `PowerBI`, `C++` vs `C#`).
3. **TF-IDF + Cosine Distance**: Discuss how n-gram TF-IDF captures broader role context (e.g. leadership, cross-functional collaboration, methodology) beyond isolated skill keywords.
4. **Actionable Recommendations**: Highlight that the tool doesn't just evaluate candidates, but provides a personalized roadmap to bridge skill gaps.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
