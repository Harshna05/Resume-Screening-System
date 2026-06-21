def extract_txt_text(file):
    """
    Extract text from TXT resumes
    """

    try:
        # Uploaded file from Streamlit
        if hasattr(file, "read"):
            return file.read().decode("utf-8", errors="ignore")

        # Normal file path
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ""