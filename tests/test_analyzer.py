"""
Unit Tests for AI Resume Analyzer & Job Matcher
Verifies PDF extraction, skill identification, TF-IDF cosine similarity,
gap detection, learning recommendations, and CSV report export.
"""

import os
import unittest
from src.pdf_extractor import clean_extracted_text, extract_text_from_pdf
from src.skill_extractor import SkillExtractor
from src.matcher import Matcher, calculate_tfidf_similarity
from src.recommender import LearningRecommender
from src.report_generator import ReportGenerator


class TestResumeAnalyzer(unittest.TestCase):

    def setUp(self):
        self.extractor = SkillExtractor()
        self.matcher = Matcher(skill_weight=0.60, text_weight=0.40)
        self.recommender = LearningRecommender()

    def test_clean_extracted_text(self):
        raw = "Experi-\nenced data scien-\ntist • with Python    and SQL\n\n\n\nMachine Learning"
        cleaned = clean_extracted_text(raw)
        self.assertIn("Experienced", cleaned)
        self.assertIn("scientist", cleaned)
        self.assertIn("Python", cleaned)
        self.assertNotIn("\n\n\n\n", cleaned)

    def test_pdf_file_extraction(self):
        pdf_path = os.path.join("sample_data", "sample_resume_data_analyst.pdf")
        if os.path.exists(pdf_path):
            extracted = extract_text_from_pdf(pdf_path)
            self.assertFalse(extracted["is_empty"])
            self.assertGreater(extracted["word_count"], 50)
            self.assertIn("Senior Data Analyst", extracted["text"])
            self.assertIn("Power BI", extracted["text"])
            self.assertEqual(extracted["num_pages"], 1)

    def test_skill_extraction_core(self):
        sample_text = """
        Experienced Data Analyst skilled in Python, SQL, Excel, and Power BI.
        Built machine learning models using Scikit-Learn and Pandas.
        Experience with React, Node.js, and Docker for deployment.
        """
        results = self.extractor.extract_skills(sample_text)
        detected = results["detected_skills"]

        # Assert specified required technologies
        self.assertIn("Python", detected)
        self.assertIn("SQL", detected)
        self.assertIn("Excel", detected)
        self.assertIn("Power BI", detected)
        self.assertIn("Scikit-learn", detected)
        self.assertIn("Pandas", detected)
        self.assertIn("React", detected)
        self.assertIn("Docker", detected)

    def test_skill_boundaries_and_aliases(self):
        # Ensure Java vs JavaScript discrimination
        text_java_only = "Core Java developer building enterprise services."
        res_java = self.extractor.extract_skills(text_java_only)
        self.assertIn("Java", res_java["detected_skills"])
        self.assertNotIn("JavaScript", res_java["detected_skills"])

        text_js_only = "Frontend engineer using JavaScript and React.js."
        res_js = self.extractor.extract_skills(text_js_only)
        self.assertIn("JavaScript", res_js["detected_skills"])
        self.assertIn("React", res_js["detected_skills"])

    def test_matcher_scores_and_gaps(self):
        resume_skills = ["Python", "SQL", "Excel", "Pandas"]
        jd_skills = ["Python", "SQL", "Power BI", "AWS", "Snowflake"]

        resume_text = "Experienced with Python and SQL data analysis using Pandas."
        jd_text = "Looking for Python, SQL, Power BI, AWS, and Snowflake developer."

        match_res = self.matcher.match(
            resume_skills=resume_skills,
            jd_skills=jd_skills,
            resume_text=resume_text,
            jd_text=jd_text
        )

        # Matched skills should be Python and SQL (2 out of 5)
        self.assertEqual(sorted(match_res["matched_skills"]), ["Python", "SQL"])
        # Missing skills should be AWS, Power BI, Snowflake
        self.assertEqual(sorted(match_res["missing_skills"]), ["AWS", "Power BI", "Snowflake"])
        # Extra skills in resume should be Excel, Pandas
        self.assertEqual(sorted(match_res["extra_skills"]), ["Excel", "Pandas"])

        # Skill coverage: 2 / 5 = 40.0%
        self.assertEqual(match_res["skill_coverage_score"], 40.0)
        self.assertGreater(match_res["text_similarity_score"], 0.0)
        self.assertGreater(match_res["overall_score"], 0.0)

    def test_tfidf_similarity(self):
        text_a = "Python software engineer building scalable web APIs with FastAPI and Docker."
        text_b = "Python software engineer building scalable web APIs with FastAPI and Docker."
        # Identical text should have ~100% similarity
        score_identical = calculate_tfidf_similarity(text_a, text_b)
        self.assertAlmostEqual(score_identical, 100.0, places=1)

        text_c = "Ancient history of Roman pottery and agricultural architecture."
        score_unrelated = calculate_tfidf_similarity(text_a, text_c)
        self.assertLess(score_unrelated, 15.0)

    def test_learning_recommender(self):
        missing = ["Power BI", "Snowflake", "Docker"]
        recs = self.recommender.get_recommendations(missing)

        self.assertEqual(len(recs), 3)
        skills_recommended = [r["skill"] for r in recs]
        self.assertIn("Power BI", skills_recommended)
        self.assertIn("Snowflake", skills_recommended)
        self.assertIn("Docker", skills_recommended)

        for r in recs:
            self.assertTrue(r["url"].startswith("http"))
            self.assertTrue(len(r["title"]) > 0)
            self.assertTrue(len(r["action_plan"]) > 0)

    def test_report_generation(self):
        match_data = {
            "matched_skills": ["Python", "SQL"],
            "missing_skills": ["Power BI"],
            "extra_skills": ["Git"],
            "skill_coverage_score": 66.7,
            "text_similarity_score": 55.0,
            "overall_score": 62.0,
            "total_jd_skills": 3,
            "total_resume_skills": 3
        }
        recs = self.recommender.get_recommendations(match_data["missing_skills"])
        df = ReportGenerator.generate_skills_dataframe(match_data, recs)

        self.assertFalse(df.empty)
        self.assertIn("Skill", df.columns)
        self.assertIn("Status", df.columns)
        self.assertIn("Action / Recommendation", df.columns)

        csv_bytes = ReportGenerator.dataframe_to_csv_bytes(df)
        self.assertTrue(len(csv_bytes) > 0)

        summary = ReportGenerator.generate_executive_summary("Alex", "Data Analyst", match_data)
        self.assertIn("Overall Weighted Match Score", summary)
        self.assertIn("Python", summary)


if __name__ == "__main__":
    unittest.main()
