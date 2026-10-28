"""
AI Resume Analyzer & Job Matcher - Streamlit Dashboard
An interactive AI web application for parsing resumes, extracting technical skills,
matching against job descriptions with TF-IDF & NLP, identifying skill gaps,
generating learning recommendations, and exporting reports.
"""

import os
import streamlit as st
import pandas as pd
from typing import Optional

# Internal modules
from src.pdf_extractor import extract_text_from_pdf
from src.skill_extractor import SkillExtractor
from src.matcher import Matcher
from src.recommender import LearningRecommender
from src.report_generator import ReportGenerator

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern UI Styling (CSS)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* Main container adjustments */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
    
    /* Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
        margin: 0;
    }
    
    /* Metric Score Card */
    .score-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }
    .score-val {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .score-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }
    
    /* Skill Badge Pills */
    .badge-matched {
        display: inline-block;
        background-color: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        padding: 4px 12px;
        margin: 3px 4px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-missing {
        display: inline-block;
        background-color: #fef2f2;
        color: #991b1b;
        border: 1px solid #fecaca;
        padding: 4px 12px;
        margin: 3px 4px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-extra {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        padding: 4px 12px;
        margin: 3px 4px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Recommendation Card */
    .rec-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .rec-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 4px;
    }
    .rec-meta {
        font-size: 0.82rem;
        color: #64748b;
        margin-bottom: 6px;
    }
    .rec-plan {
        font-size: 0.88rem;
        color: #334155;
        background-color: #f8fafc;
        padding: 6px 10px;
        border-radius: 6px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_source_name" not in st.session_state:
    st.session_state.resume_source_name = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None


# ---------------------------------------------------------
# Sidebar Controls & Information
# ---------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.markdown("### 📊 Matching Weights")
    skill_weight = st.slider(
        "Skill Coverage Weight",
        min_value=0.0,
        max_value=1.0,
        value=0.60,
        step=0.05,
        help="Weight assigned to exact technical skill matches in overall score."
    )
    text_weight = round(1.0 - skill_weight, 2)
    st.caption(f"Text Similarity (TF-IDF) Weight: **{text_weight * 100:.0f}%**")
    
    st.markdown("---")
    st.markdown("### 📁 Load Sample Examples")
    st.caption("Quickly test the system without uploading a file:")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("📊 Data Analyst", use_container_width=True):
            try:
                res_path = os.path.join("sample_data", "sample_resume_data_analyst.txt")
                jd_path = os.path.join("sample_data", "sample_jd_data_analyst.txt")
                with open(res_path, "r", encoding="utf-8") as f:
                    st.session_state.resume_text = f.read()
                st.session_state.resume_source_name = "Sample: Data Analyst Resume"
                with open(jd_path, "r", encoding="utf-8") as f:
                    st.session_state.jd_text = f.read()
                st.session_state.analysis_results = None
                st.success("Loaded Data Analyst Sample!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading sample: {e}")
                
    with col_s2:
        if st.button("💻 Full Stack Dev", use_container_width=True):
            try:
                res_path = os.path.join("sample_data", "sample_resume_software_engineer.txt")
                jd_path = os.path.join("sample_data", "sample_jd_software_engineer.txt")
                with open(res_path, "r", encoding="utf-8") as f:
                    st.session_state.resume_text = f.read()
                st.session_state.resume_source_name = "Sample: Software Engineer Resume"
                with open(jd_path, "r", encoding="utf-8") as f:
                    st.session_state.jd_text = f.read()
                st.session_state.analysis_results = None
                st.success("Loaded Full Stack Sample!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading sample: {e}")

    if st.button("🧹 Clear All Inputs", use_container_width=True):
        st.session_state.resume_text = ""
        st.session_state.resume_source_name = ""
        st.session_state.jd_text = ""
        st.session_state.analysis_results = None
        st.rerun()

    st.markdown("---")
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("""
    - **Streamlit** (UI & Dashboard)
    - **PyMuPDF** (PDF Parsing)
    - **spaCy & Regex** (Skill Extraction)
    - **Scikit-learn** (TF-IDF & Cosine Similarity)
    - **Pandas** (Report Analytics)
    """)
    st.caption("v1.0.0 | Offline NLP & Rule-based Matcher")


# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🎯 AI Resume Analyzer & Job Matcher</div>
    <div class="hero-subtitle">
        Upload your resume (PDF) and paste a target job description to compute skill coverage,
        discover alignment scores, identify missing competencies, and receive curated learning paths.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Input Section: Resume Upload & Job Description
# ---------------------------------------------------------
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("1. Resume Input")
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF format)",
        type=["pdf"],
        help="Upload your resume in PDF. Text will be cleanly extracted via PyMuPDF."
    )
    
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF using PyMuPDF..."):
            extracted = extract_text_from_pdf(uploaded_file)
            if extracted["error"]:
                st.error(f"PDF Extraction Failed: {extracted['error']}")
            elif extracted["is_empty"]:
                st.warning("⚠️ No extractable text found in this PDF. It might be a scanned image.")
            else:
                st.session_state.resume_text = extracted["text"]
                st.session_state.resume_source_name = uploaded_file.name
                st.success(f"Extracted {extracted['word_count']} words across {extracted['num_pages']} page(s).")
    
    # Text area or preview
    resume_display_text = st.text_area(
        "Resume Text Preview / Manual Edit:",
        value=st.session_state.resume_text,
        height=260,
        help="You can review the extracted text or paste/edit resume text manually."
    )
    # Sync manual changes
    st.session_state.resume_text = resume_display_text


with col_right:
    st.subheader("2. Target Job Description")
    jd_input = st.text_area(
        "Paste Job Description / Requirements:",
        value=st.session_state.jd_text,
        height=322,
        placeholder="Paste role requirements, responsibilities, or complete job posting here..."
    )
    st.session_state.jd_text = jd_input
    
    word_count_jd = len(jd_input.split()) if jd_input.strip() else 0
    st.caption(f"Job Description Word Count: **{word_count_jd}** words")


# ---------------------------------------------------------
# Action Button: Analyze & Match
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])

with btn_col2:
    analyze_clicked = st.button("🚀 Analyze & Match Resume", type="primary", use_container_width=True)

if analyze_clicked:
    if not st.session_state.resume_text.strip():
        st.error("Please upload a resume or paste resume text first.")
    elif not st.session_state.jd_text.strip():
        st.error("Please paste the job description to match against.")
    else:
        with st.spinner("Analyzing skills, computing TF-IDF similarity, and generating learning roadmaps..."):
            # 1. Initialize Engines
            extractor = SkillExtractor()
            matcher = Matcher(skill_weight=skill_weight, text_weight=text_weight)
            recommender = LearningRecommender()
            
            # 2. Extract Skills
            resume_extracted = extractor.extract_skills(st.session_state.resume_text)
            jd_extracted = extractor.extract_skills(st.session_state.jd_text)
            
            # 3. Match and Calculate Scores
            match_data = matcher.match(
                resume_skills=resume_extracted["detected_skills"],
                jd_skills=jd_extracted["detected_skills"],
                resume_text=st.session_state.resume_text,
                jd_text=st.session_state.jd_text
            )
            
            # 4. Generate Recommendations for Missing Skills
            recommendations = recommender.get_recommendations(match_data["missing_skills"])
            
            # 5. Generate Report DataFrame
            skills_df = ReportGenerator.generate_skills_dataframe(match_data, recommendations)
            csv_bytes = ReportGenerator.dataframe_to_csv_bytes(skills_df)
            exec_summary = ReportGenerator.generate_executive_summary(
                candidate_name=st.session_state.resume_source_name or "Applicant",
                job_title="Target Position",
                match_results=match_data
            )
            
            # Save into session state
            st.session_state.analysis_results = {
                "resume_extracted": resume_extracted,
                "jd_extracted": jd_extracted,
                "match_data": match_data,
                "recommendations": recommendations,
                "skills_df": skills_df,
                "csv_bytes": csv_bytes,
                "exec_summary": exec_summary
            }
            st.success("Analysis complete! Review your results below.")


# ---------------------------------------------------------
# Results Dashboard Display
# ---------------------------------------------------------
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    match_data = res["match_data"]
    recs = res["recommendations"]
    skills_df = res["skills_df"]
    
    st.markdown("---")
    st.header("📊 Alignment Dashboard & Analytics")
    
    # KPI Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    
    overall = match_data["overall_score"]
    skill_cov = match_data["skill_coverage_score"]
    text_sim = match_data["text_similarity_score"]
    matched_count = len(match_data["matched_skills"])
    total_jd = match_data["total_jd_skills"]
    missing_count = len(match_data["missing_skills"])
    
    # Dynamic status color
    if overall >= 75:
        color = "#10b981"
        badge_text = "🟢 Strong Fit"
    elif overall >= 50:
        color = "#f59e0b"
        badge_text = "🟡 Moderate Fit"
    else:
        color = "#ef4444"
        badge_text = "🔴 Needs Upskilling"
        
    with m1:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-val" style="color: {color};">{overall:.1f}%</div>
            <div class="score-label">Overall Match Score</div>
            <div style="font-size: 0.8rem; margin-top: 4px; font-weight: 600;">{badge_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-val" style="color: #2563eb;">{skill_cov:.1f}%</div>
            <div class="score-label">Skill Coverage</div>
            <div style="font-size: 0.8rem; margin-top: 4px; color: #64748b;">{matched_count} of {total_jd} skills</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-val" style="color: #7c3aed;">{text_sim:.1f}%</div>
            <div class="score-label">TF-IDF Similarity</div>
            <div style="font-size: 0.8rem; margin-top: 4px; color: #64748b;">Cosine textual distance</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-val" style="color: #dc2626;">{missing_count}</div>
            <div class="score-label">Missing Skills</div>
            <div style="font-size: 0.8rem; margin-top: 4px; color: #64748b;">Targeted growth areas</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Download Toolbar
    dl_c1, dl_c2 = st.columns([1, 1])
    with dl_c1:
        st.download_button(
            label="📥 Download Detailed CSV Report",
            data=res["csv_bytes"],
            file_name="resume_job_match_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    with dl_c2:
        st.download_button(
            label="📄 Download Summary Text (Markdown)",
            data=res["exec_summary"],
            file_name="resume_match_executive_summary.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for in-depth exploration
    tab_skills, tab_recs, tab_table, tab_breakdown = st.tabs([
        "🏷️ Skills Breakdown",
        "💡 Learning Recommendations",
        "📋 Full Comparison Table",
        "📈 Domain Category Analysis"
    ])

    # TAB 1: Skills Breakdown
    with tab_skills:
        col_matched, col_missing, col_extra = st.columns(3)
        
        with col_matched:
            st.markdown(f"#### ✅ Matched Skills ({len(match_data['matched_skills'])})")
            st.caption("Skills found in both resume and job description:")
            if match_data["matched_skills"]:
                badges = "".join([f'<span class="badge-matched">✓ {s}</span>' for s in match_data["matched_skills"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.info("No matching skills detected.")
                
        with col_missing:
            st.markdown(f"#### ⚠️ Missing Skills ({len(match_data['missing_skills'])})")
            st.caption("Required by job description, not found in resume:")
            if match_data["missing_skills"]:
                badges = "".join([f'<span class="badge-missing">✗ {s}</span>' for s in match_data["missing_skills"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.success("🎉 Awesome! You match 100% of the required skills.")

        with col_extra:
            st.markdown(f"#### 🌟 Additional Skills ({len(match_data['extra_skills'])})")
            st.caption("Found in your resume, beyond stated requirements:")
            if match_data["extra_skills"]:
                badges = "".join([f'<span class="badge-extra">+ {s}</span>' for s in match_data["extra_skills"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.caption("No extra skills found.")

    # TAB 2: Learning Recommendations
    with tab_recs:
        st.markdown("#### 🚀 Actionable Learning Pathways for Skill Gaps")
        if not recs:
            st.success("No missing skills! No immediate upskilling required for this role.")
        else:
            st.caption(f"Identified {len(recs)} skill gaps. Click any link to start studying:")
            for item in recs:
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-title">🎯 {item['skill']} <span style="font-size:0.8rem; font-weight:normal; color:#64748b;">({item['category']})</span></div>
                    <div class="rec-meta">
                        📚 Resource: <a href="{item['url']}" target="_blank"><b>{item['title']}</b></a> | 
                        🏢 Platform: <b>{item['platform']}</b> | 
                        ⏱️ Est. Time: <b>{item['estimated_time']}</b>
                    </div>
                    <div class="rec-plan">
                        <b>Suggested Action Plan:</b> {item['action_plan']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # TAB 3: Full Comparison Table
    with tab_table:
        st.markdown("#### 📑 Comprehensive Skill Alignment Data")
        st.dataframe(
            skills_df,
            use_container_width=True,
            hide_index=True
        )

    # TAB 4: Category Analysis
    with tab_breakdown:
        st.markdown("#### 📊 Domain Alignment Breakdown")
        st.caption("Comparison of requirements across technical categories:")
        cat_data = []
        for cat, vals in match_data.get("category_breakdown", {}).items():
            if vals["jd_required"] > 0 or vals["matched"] > 0:
                pct = round((vals["matched"] / vals["jd_required"] * 100), 1) if vals["jd_required"] > 0 else 100.0
                cat_data.append({
                    "Category": cat,
                    "Required by JD": vals["jd_required"],
                    "Matched in Resume": vals["matched"],
                    "Missing": vals["missing"],
                    "Category Coverage": f"{pct}%"
                })
        if cat_data:
            cat_df = pd.DataFrame(cat_data)
            st.dataframe(cat_df, use_container_width=True, hide_index=True)
            # Display a Streamlit bar chart of Required vs Matched
            chart_df = cat_df.set_index("Category")[["Required by JD", "Matched in Resume"]]
            st.bar_chart(chart_df)
        else:
            st.info("No categorical skill patterns detected.")
