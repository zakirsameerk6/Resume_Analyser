"""
Report Generation Engine using Pandas.
Exports structured CSV analysis reports, skill gap breakdowns,
and executive summaries for job applications.
"""

from typing import Dict, List, Any
import pandas as pd
from datetime import datetime


class ReportGenerator:
    """
    Constructs Pandas DataFrames and downloadable CSV / text summaries
    from analysis outcomes.
    """

    @staticmethod
    def generate_skills_dataframe(
        match_results: Dict[str, Any],
        recommendations: List[Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        Creates a structured Pandas DataFrame detailing all analyzed skills,
        their status (Matched, Missing, Extra), category, and learning resources.
        """
        rec_lookup = {r["skill"]: r for r in recommendations}
        records = []

        # 1. Matched Skills
        for skill in match_results.get("matched_skills", []):
            records.append({
                "Skill": skill,
                "Status": "Matched (Found in Resume & JD)",
                "Category": rec_lookup.get(skill, {}).get("category", "General"),
                "Priority": "Aligned",
                "Action / Recommendation": "Highlight in bullet points and interview talking points",
                "Learning Resource": rec_lookup.get(skill, {}).get("url", "N/A"),
                "Platform": rec_lookup.get(skill, {}).get("platform", "N/A")
            })

        # 2. Missing Skills (Gaps)
        for skill in match_results.get("missing_skills", []):
            rec = rec_lookup.get(skill, {})
            records.append({
                "Skill": skill,
                "Status": "Missing in Resume (Required by JD)",
                "Category": rec.get("category", "General"),
                "Priority": "High (Upskill Needed)",
                "Action / Recommendation": rec.get("action_plan", "Learn fundamentals & build a project"),
                "Learning Resource": rec.get("url", "N/A"),
                "Platform": rec.get("platform", "N/A")
            })

        # 3. Extra Skills (Bonus in Resume)
        for skill in match_results.get("extra_skills", []):
            records.append({
                "Skill": skill,
                "Status": "Candidate Bonus (In Resume, not requested in JD)",
                "Category": "Additional Strength",
                "Priority": "Bonus Competency",
                "Action / Recommendation": "Demonstrates broader versatility",
                "Learning Resource": "N/A",
                "Platform": "N/A"
            })

        df = pd.DataFrame(records)
        return df

    @staticmethod
    def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
        """Converts Pandas DataFrame to CSV bytes for Streamlit download button."""
        return df.to_csv(index=False).encode("utf-8")

    @staticmethod
    def generate_executive_summary(
        candidate_name: str,
        job_title: str,
        match_results: Dict[str, Any]
    ) -> str:
        """
        Generates an executive plain-text / markdown summary of the match analysis.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        matched = match_results.get("matched_skills", [])
        missing = match_results.get("missing_skills", [])
        extra = match_results.get("extra_skills", [])

        summary = f"""# AI Resume Analysis & Job Match Report
Generated: {timestamp}
Target Role: {job_title or 'Target Job Description'}
Candidate: {candidate_name or 'Applicant'}

## 1. Key Alignment Metrics
- Overall Weighted Match Score: {match_results.get('overall_score', 0):.1f}%
- Skill Coverage Score: {match_results.get('skill_coverage_score', 0):.1f}% ({len(matched)} / {match_results.get('total_jd_skills', 0)} required skills matched)
- TF-IDF Text Similarity: {match_results.get('text_similarity_score', 0):.1f}%

## 2. Matched Skills ({len(matched)})
{', '.join(matched) if matched else 'None detected'}

## 3. Skill Gaps / Missing Competencies ({len(missing)})
{', '.join(missing) if missing else 'None! Complete skill match.'}

## 4. Additional Strengths / Bonus Skills ({len(extra)})
{', '.join(extra) if extra else 'None detected'}

---
Note: This analysis utilizes NLP tokenization, regex matching, and TF-IDF cosine similarity.
"""
        return summary
