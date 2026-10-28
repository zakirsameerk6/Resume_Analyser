"""
Learning Recommendation Engine.
Maps missing skills to high-quality curated learning resources,
documentation, official roadmaps, and estimated time to acquire proficiency.
"""

from typing import List, Dict, Any
from src.skill_database import SKILL_TAXONOMY, get_default_recommendation


class LearningRecommender:
    """
    Generates tailored learning roadmaps for missing job competencies.
    """

    def __init__(self, taxonomy: Dict[str, Dict[str, Any]] = None):
        self.taxonomy = taxonomy or SKILL_TAXONOMY

    def get_recommendations(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Generates structured learning pathways for all missing skills.

        Returns:
            List of dicts: [
                {
                    "skill": "Power BI",
                    "category": "BI & Analytics",
                    "title": "Microsoft Power BI Guided Learning",
                    "url": "https://...",
                    "platform": "Microsoft Learn",
                    "type": "Hands-on Learning Path",
                    "estimated_time": "2 weeks",
                    "action_plan": "..."
                },
                ...
            ]
        """
        recommendations = []

        for skill in missing_skills:
            info = self.taxonomy.get(skill)
            if info and "resource" in info:
                res = info["resource"]
                cat = info.get("category", "General")
                action_plan = self._generate_action_plan(skill, cat)
                recommendations.append({
                    "skill": skill,
                    "category": cat,
                    "title": res.get("title", f"Learn {skill}"),
                    "url": res.get("url", f"https://www.google.com/search?q={skill}+tutorial"),
                    "platform": res.get("platform", "Online Resource"),
                    "type": res.get("type", "Course / Documentation"),
                    "estimated_time": res.get("estimated_time", "1-2 weeks"),
                    "action_plan": action_plan
                })
            else:
                fallback = get_default_recommendation(skill)
                recommendations.append({
                    "skill": skill,
                    "category": "Domain Competency",
                    "title": fallback["title"],
                    "url": fallback["url"],
                    "platform": fallback["platform"],
                    "type": fallback["type"],
                    "estimated_time": fallback["estimated_time"],
                    "action_plan": f"Review core documentation and complete 1 practical project utilizing {skill}."
                })

        return recommendations

    def _generate_action_plan(self, skill: str, category: str) -> str:
        """Generates pragmatic project-based advice for each skill."""
        if category == "Programming Languages":
            return f"Review syntax & standard library on {skill}, then solve 10 algorithmic problems and build a CLI or script."
        elif category in ["BI & Analytics", "Data Analysis"]:
            return f"Import a messy dataset, build clean calculated columns/measures, and construct an interactive 3-tab dashboard."
        elif category in ["Databases & Data Engineering"]:
            return f"Design a normalized schema, write complex JOINs/window functions or aggregations, and optimize query indexing."
        elif category in ["Machine Learning & AI", "Data Science Libraries"]:
            return f"Build an end-to-end pipeline: data preprocessing, model training, evaluation metrics, and hyperparameter tuning."
        elif category == "Cloud & DevOps":
            return f"Set up a local environment or free-tier cloud account, containerize a small app, and automate deployment via pipeline."
        elif category == "Web Development":
            return f"Construct a responsive full-stack or frontend feature with state management and REST API integration."
        else:
            return f"Study fundamental concepts, observe real-world case studies, and apply principles to a portfolio project."
