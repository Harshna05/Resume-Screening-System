from parser.pdf_parser import extract_pdf_text
from utils.skills_extractor import extract_skills

resume_text = extract_pdf_text(
    "sample_resume.pdf"
)

skills = extract_skills(
    resume_text
)

print("Skills Found:")
print(skills)