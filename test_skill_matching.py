from parser.pdf_parser import extract_pdf_text
from utils.skill_matcher import compare_skills

job_description = """
Looking for a Python Developer.

Required Skills:

Python
Django
SQL
AWS
Docker
Git
"""

resume_text = extract_pdf_text(
    "sample_resume.pdf"
)

matched, missing = compare_skills(
    job_description,
    resume_text
)

print("Matched Skills:")
print(matched)

print("\nMissing Skills:")
print(missing)