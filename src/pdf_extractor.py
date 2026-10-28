"""
PDF Text Extraction Module using PyMuPDF (fitz).
Supports reading from file paths or memory buffers (Streamlit UploadedFile),
with text sanitization, page inspection, and statistics.
"""

import re
from typing import Dict, Any, Union, BinaryIO
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_source: Union[str, bytes, BinaryIO]) -> Dict[str, Any]:
    """
    Extracts structured text and metadata from a PDF file.

    Args:
        pdf_source: File path (str), raw bytes (bytes), or file-like object (BytesIO).

    Returns:
        dict: {
            "text": str,              # Extracted and normalized full text
            "num_pages": int,         # Page count
            "char_count": int,        # Total character count
            "word_count": int,        # Total word count
            "pages": List[str],       # Text separated per page
            "is_empty": bool,         # Flag if no text extracted (e.g. scanned image)
            "error": Optional[str]    # Error description if any occurred
        }
    """
    result = {
        "text": "",
        "num_pages": 0,
        "char_count": 0,
        "word_count": 0,
        "pages": [],
        "is_empty": True,
        "error": None
    }

    try:
        # Determine source type
        if isinstance(pdf_source, str):
            doc = fitz.open(pdf_source)
        elif isinstance(pdf_source, bytes):
            doc = fitz.open(stream=pdf_source, filetype="pdf")
        elif hasattr(pdf_source, "read"):
            # BytesIO or Streamlit UploadedFile
            stream_bytes = pdf_source.read()
            # Reset seek if needed
            if hasattr(pdf_source, "seek"):
                pdf_source.seek(0)
            doc = fitz.open(stream=stream_bytes, filetype="pdf")
        else:
            raise ValueError("Unsupported PDF source type. Must be path, bytes, or file-like object.")

        result["num_pages"] = len(doc)
        page_texts = []

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            page_text = page.get_text("text")
            cleaned_page = clean_extracted_text(page_text)
            page_texts.append(cleaned_page)

        doc.close()

        full_text = "\n\n".join(filter(None, page_texts)).strip()
        result["pages"] = page_texts
        result["text"] = full_text
        result["char_count"] = len(full_text)
        result["word_count"] = len(full_text.split())
        result["is_empty"] = (len(full_text.strip()) == 0)

    except Exception as e:
        result["error"] = str(e)
        result["is_empty"] = True

    return result


def clean_extracted_text(text: str) -> str:
    """
    Cleans raw PDF text: fixes hyphenated linebreaks, removes strange symbols,
    normalizes whitespace and bullet points.
    """
    if not text:
        return ""

    # Replace weird unicode bullets and symbols
    text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\uf0b7]", "\n• ", text)
    # Join hyphenated words split across lines (e.g., 'engi-\nneer' -> 'engineer')
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)
    # Normalize multiple line breaks to max 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Normalize excessive tabs and spaces
    text = re.sub(r"[ \t]+", " ", text)
    # Remove control characters except standard whitespace
    text = "".join(ch for ch in text if ch == "\n" or ch == "\t" or (32 <= ord(ch) <= 126) or ord(ch) > 160)

    return text.strip()
