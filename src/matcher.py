"""
Resume & Job Description Matching Engine.
Calculates Skill Coverage, TF-IDF Cosine Similarity,
identifies matched/missing/extra skills, and computes domain-wise alignment.
"""

from typing import Dict, List, Set, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.skill_database import SKILL_TAXONOMY


def calculate_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculates Cosine Similarity between resume text and job description using TF-IDF.
    
    Returns:
        float: Similarity percentage from 0.0 to 100.0.
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    try:
        # Stopwords 'english' with n-gram range (1, 2) for unigrams and bigrams
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(similarity_matrix[0][0]) * 100.0
        return round(max(0.0, min(100.0, score)), 2)
    except Exception:
        # Fallback in case of empty vocabulary after stopword removal
        return 0.0


class Matcher:
    """
    Computes comparative analysis between candidate resume and target job description.
    """

    def __init__(self, skill_weight: float = 0.60, text_weight: float = 0.40):
        """
        Args:
            skill_weight: Weight for skill coverage in overall score (default 0.60)
            text_weight: Weight for TF-IDF similarity in overall score (default 0.40)
        """
        self.skill_weight = skill_weight
        self.text_weight = text_weight

    def match(
        self,
        resume_skills: List[str],
        jd_skills: List[str],
        resume_text: str,
        jd_text: str
    ) -> Dict[str, Any]:
        """
        Executes complete matching analysis.

        Returns:
            dict: {
                "skill_coverage_score": float (0-100),
                "text_similarity_score": float (0-100),
                "overall_score": float (0-100),
                "matched_skills": List[str],
                "missing_skills": List[str],
                "extra_skills": List[str],
                "total_jd_skills": int,
                "total_resume_skills": int,
                "category_breakdown": Dict[str, Dict[str, int]]
            }
        """
        resume_set = set(resume_skills)
        jd_set = set(jd_skills)

        # 1. Skills Comparison
        matched_set = resume_set.intersection(jd_set)
        missing_set = jd_set.difference(resume_set)
        extra_set = resume_set.difference(jd_set)

        matched_skills = sorted(list(matched_set))
        missing_skills = sorted(list(missing_set))
        extra_skills = sorted(list(extra_set))

        # 2. Skill Coverage Score
        if len(jd_set) > 0:
            skill_coverage = round((len(matched_set) / len(jd_set)) * 100.0, 2)
        else:
            # If JD had no specific skills detected, default coverage to 0 or 100 depending on content
            skill_coverage = 0.0 if not jd_text.strip() else 50.0

        # 3. TF-IDF Cosine Similarity Score
        text_similarity = calculate_tfidf_similarity(resume_text, jd_text)

        # 4. Overall Weighted Score
        overall_score = round(
            (skill_coverage * self.skill_weight) + (text_similarity * self.text_weight),
            2
        )

        # 5. Category-wise Breakdown
        category_breakdown = {}
        all_relevant_skills = jd_set.union(resume_set)

        for skill in all_relevant_skills:
            cat = SKILL_TAXONOMY.get(skill, {}).get("category", "Other")
            if cat not in category_breakdown:
                category_breakdown[cat] = {"matched": 0, "missing": 0, "extra": 0, "jd_required": 0}

            if skill in jd_set:
                category_breakdown[cat]["jd_required"] += 1

            if skill in matched_set:
                category_breakdown[cat]["matched"] += 1
            elif skill in missing_set:
                category_breakdown[cat]["missing"] += 1
            elif skill in extra_set:
                category_breakdown[cat]["extra"] += 1

        return {
            "skill_coverage_score": skill_coverage,
            "text_similarity_score": text_similarity,
            "overall_score": overall_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills,
            "total_jd_skills": len(jd_set),
            "total_resume_skills": len(resume_set),
            "category_breakdown": category_breakdown
        }
