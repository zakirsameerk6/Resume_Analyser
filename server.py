"""
FastAPI Backend Server for AI Resume Analyzer & Job Matcher.
Provides REST endpoints for PDF text extraction, skill analysis,
matching calculation, learning recommendations, and CSV/summary report export.
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel

# Internal logic
from src.pdf_extractor import extract_text_from_pdf
from src.skill_extractor import SkillExtractor
from src.matcher import Matcher
from src.recommender import LearningRecommender
from src.report_generator import ReportGenerator

app = FastAPI(
    title="AI Resume Analyzer & Job Matcher API",
    description="High-performance NLP and skill matching API",
    version="1.0.0"
)

# Enable CORS for React/Vite development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
extractor = SkillExtractor()
recommender = LearningRecommender()


class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str
    skill_weight: Optional[float] = 0.60
    text_weight: Optional[float] = 0.40
    candidate_name: Optional[str] = "Candidate"
    job_title: Optional[str] = "Target Role"


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Resume Analyzer API", "version": "1.0.0"}


@app.get("/api/samples")
def get_sample_data():
    """Returns pre-loaded sample resumes and job descriptions."""
    samples = {}
    sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data")
    
    files = {
        "data_analyst_resume": "sample_resume_data_analyst.txt",
        "data_analyst_jd": "sample_jd_data_analyst.txt",
        "software_engineer_resume": "sample_resume_software_engineer.txt",
        "software_engineer_jd": "sample_jd_software_engineer.txt"
    }

    for key, filename in files.items():
        path = os.path.join(sample_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                samples[key] = f.read()
        else:
            samples[key] = ""

    return samples


@app.post("/api/upload-resume")
async def upload_resume_pdf(file: UploadFile = File(...)):
    """
    Accepts PDF upload, extracts text with PyMuPDF, and returns extracted text & metadata.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        content = await file.read()
        extracted = extract_text_from_pdf(content)

        if extracted["error"]:
            raise HTTPException(status_code=400, detail=f"PDF extraction error: {extracted['error']}")
        
        # Pre-extract skills from resume
        skills = extractor.extract_skills(extracted["text"])

        return {
            "filename": file.filename,
            "text": extracted["text"],
            "num_pages": extracted["num_pages"],
            "word_count": extracted["word_count"],
            "is_empty": extracted["is_empty"],
            "detected_skills": skills["detected_skills"],
            "categorized_skills": skills["categorized"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


@app.post("/api/match")
def match_resume(req: MatchRequest):
    """
    Computes Skill Coverage, TF-IDF Cosine Similarity, gap analysis,
    and learning recommendations.
    """
    if not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")
    if not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")

    # 1. Extract skills from both documents
    resume_skills_data = extractor.extract_skills(req.resume_text)
    jd_skills_data = extractor.extract_skills(req.jd_text)

    # 2. Match
    skill_w = req.skill_weight if req.skill_weight is not None else 0.60
    text_w = req.text_weight if req.text_weight is not None else 0.40
    matcher = Matcher(skill_weight=skill_w, text_weight=text_w)

    match_results = matcher.match(
        resume_skills=resume_skills_data["detected_skills"],
        jd_skills=jd_skills_data["detected_skills"],
        resume_text=req.resume_text,
        jd_text=req.jd_text
    )

    # 3. Recommendations
    recommendations = recommender.get_recommendations(match_results["missing_skills"])

    # 4. Summary & Table data
    skills_df = ReportGenerator.generate_skills_dataframe(match_results, recommendations)
    table_records = skills_df.to_dict(orient="records")

    exec_summary = ReportGenerator.generate_executive_summary(
        candidate_name=req.candidate_name or "Candidate",
        job_title=req.job_title or "Target Position",
        match_results=match_results
    )

    return {
        "match_results": match_results,
        "resume_skills": resume_skills_data,
        "jd_skills": jd_skills_data,
        "recommendations": recommendations,
        "table_records": table_records,
        "exec_summary": exec_summary
    }


@app.post("/api/export-csv")
def export_csv(req: MatchRequest):
    """Generates and downloads a CSV report."""
    resume_skills_data = extractor.extract_skills(req.resume_text)
    jd_skills_data = extractor.extract_skills(req.jd_text)
    matcher = Matcher(skill_weight=req.skill_weight or 0.60, text_weight=req.text_weight or 0.40)

    match_results = matcher.match(
        resume_skills=resume_skills_data["detected_skills"],
        jd_skills=jd_skills_data["detected_skills"],
        resume_text=req.resume_text,
        jd_text=req.jd_text
    )
    recommendations = recommender.get_recommendations(match_results["missing_skills"])
    df = ReportGenerator.generate_skills_dataframe(match_results, recommendations)
    csv_bytes = ReportGenerator.dataframe_to_csv_bytes(df)

    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="resume_job_match_report.csv"'}
    )


# Mount built React frontend if dist directory exists
frontend_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "dist")
if os.path.exists(frontend_dist):
    from fastapi.staticfiles import StaticFiles
    app.mount("/resumeanalyser", StaticFiles(directory=frontend_dist, html=True), name="resumeanalyser")
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
