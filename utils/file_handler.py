from parser.pdf_parser import extract_pdf_text
from parser.docx_parser import extract_docx_text
from parser.txt_parser import extract_txt_text


def extract_text(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(uploaded_file)

    elif filename.endswith(".docx"):
        return extract_docx_text(uploaded_file)

    elif filename.endswith(".txt"):
        return extract_txt_text(uploaded_file)

    return ""