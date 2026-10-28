"""
Generates sample PDF resumes in sample_data/ using PyMuPDF.
Enables instant testing with actual PDF file uploads in Streamlit.
"""

import os
import fitz  # PyMuPDF


def create_pdf(text_file_path: str, output_pdf_path: str, title: str):
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 standard points
    
    with open(text_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define rect for page margins
    rect = fitz.Rect(50, 50, 545, 792)

    # Insert text into page
    page.insert_textbox(
        rect,
        content,
        fontsize=10,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=0
    )

    doc.save(output_pdf_path)
    doc.close()
    print(f"Created: {output_pdf_path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_dir = os.path.join(base_dir, "sample_data")
    
    # 1. Data Analyst PDF
    txt_da = os.path.join(sample_dir, "sample_resume_data_analyst.txt")
    pdf_da = os.path.join(sample_dir, "sample_resume_data_analyst.pdf")
    if os.path.exists(txt_da):
        create_pdf(txt_da, pdf_da, "Alex Turner - Data Analyst")

    # 2. Software Engineer PDF
    txt_se = os.path.join(sample_dir, "sample_resume_software_engineer.txt")
    pdf_se = os.path.join(sample_dir, "sample_resume_software_engineer.pdf")
    if os.path.exists(txt_se):
        create_pdf(txt_se, pdf_se, "Priya Sharma - Software Engineer")


if __name__ == "__main__":
    main()
