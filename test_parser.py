from parser.pdf_parser import extract_pdf_text

print("Starting...")

text = extract_pdf_text("sample_resume.pdf")

print("Extracted Text:")
print(text)

print("Length:", len(text))