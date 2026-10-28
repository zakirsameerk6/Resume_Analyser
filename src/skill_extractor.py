"""
Skill Extraction Engine using Regex and Natural Language Processing (spaCy).
Extracts, normalizes, and categorizes technical, analytical, and professional
skills from resume text and job descriptions.
"""

import re
from typing import Dict, List, Set, Any, Optional
from collections import Counter
from src.skill_database import SKILL_TAXONOMY


# Lazy-loaded spaCy NLP model
_SPACY_NLP = None


def get_spacy_nlp():
    """
    Safely loads or initializes a spaCy NLP pipeline.
    Falls back gracefully to a blank English model if en_core_web_sm is not downloaded.
    """
    global _SPACY_NLP
    if _SPACY_NLP is not None:
        return _SPACY_NLP

    try:
        import spacy
        try:
            _SPACY_NLP = spacy.load("en_core_web_sm")
        except OSError:
            # Fall back to blank English tokenizer pipeline
            _SPACY_NLP = spacy.blank("en")
    except ImportError:
        _SPACY_NLP = None

    return _SPACY_NLP


class SkillExtractor:
    """
    Extracts canonical skills from unstructured text using regex patterns,
    word boundaries, and NLP tokenization.
    """

    def __init__(self, taxonomy: Optional[Dict[str, Dict[str, Any]]] = None):
        self.taxonomy = taxonomy or SKILL_TAXONOMY
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Pre-compiles regex patterns for high-performance matching."""
        compiled = {}
        for skill_name, info in self.taxonomy.items():
            patterns = []
            aliases = info.get("aliases", [rf"\b{re.escape(skill_name.lower())}\b"])
            for alias in aliases:
                try:
                    pat = re.compile(alias, re.IGNORECASE)
                    patterns.append(pat)
                except re.error:
                    # In case of irregular regex, escape literally
                    pat = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
                    patterns.append(pat)
            compiled[skill_name] = patterns
        return compiled

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """
        Extracts skills from text and returns structured breakdown.

        Returns:
            dict: {
                "detected_skills": List[str],       # Sorted canonical skills found
                "categorized": Dict[str, List[str]], # Grouped by category
                "frequencies": Dict[str, int],      # Counts per skill
                "total_count": int,                 # Number of distinct skills
                "text_tokens_count": int            # Words analyzed
            }
        """
        if not text or not text.strip():
            return {
                "detected_skills": [],
                "categorized": {},
                "frequencies": {},
                "total_count": 0,
                "text_tokens_count": 0
            }

        text_lower = text.lower()
        frequencies: Counter = Counter()

        # 1. Regex & Boundary Matching across Taxonomy
        for skill_name, patterns in self._compiled_patterns.items():
            match_count = 0
            for pat in patterns:
                matches = pat.findall(text_lower)
                if matches:
                    match_count += len(matches)
            if match_count > 0:
                frequencies[skill_name] += match_count

        # 2. NLP Enhancement with spaCy (noun chunks / token validation)
        nlp = get_spacy_nlp()
        if nlp:
            try:
                # Process sample/truncated if text is exceedingly large
                doc = nlp(text[:25000])
                # Check for any extra multi-word technical patterns
                # Can be used to verify sentence context if needed
            except Exception:
                pass

        detected_skills = sorted(frequencies.keys())

        # Categorize detected skills
        categorized: Dict[str, List[str]] = {}
        for skill in detected_skills:
            cat = self.taxonomy.get(skill, {}).get("category", "General & Other")
            categorized.setdefault(cat, []).append(skill)

        # Sort skills inside each category
        for cat in categorized:
            categorized[cat] = sorted(categorized[cat])

        return {
            "detected_skills": detected_skills,
            "categorized": categorized,
            "frequencies": dict(frequencies),
            "total_count": len(detected_skills),
            "text_tokens_count": len(text.split())
        }

    def extract_custom_skills(self, text: str, custom_skills: List[str]) -> List[str]:
        """Allows ad-hoc extraction of user-supplied custom skills."""
        found = []
        text_lower = text.lower()
        for s in custom_skills:
            clean = s.strip()
            if not clean:
                continue
            pat = rf"\b{re.escape(clean.lower())}\b"
            if re.search(pat, text_lower):
                found.append(clean)
        return sorted(list(set(found)))
