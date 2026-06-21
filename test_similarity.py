from parser.pdf_parser import extract_pdf_text
from preprocessing.text_cleaner import preprocess_text
from ranking.similarity import calculate_similarity

job_description = """
Looking for a Python Developer.

Skills Required:

Python
Django
SQL
Git
REST API
"""

resume_text = extract_pdf_text(
    "sample_resume.pdf"
)

clean_resume = preprocess_text(
    resume_text
)

clean_job = preprocess_text(
    job_description
)

score = calculate_similarity(
    clean_job,
    clean_resume
)

print(f"Match Score: {score}%")