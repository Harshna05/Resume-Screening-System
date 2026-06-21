from parser.pdf_parser import extract_pdf_text
from preprocessing.text_cleaner import preprocess_text

text = extract_pdf_text("sample_resume.pdf")

cleaned_text = preprocess_text(text)

print(cleaned_text)