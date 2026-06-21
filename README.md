# Resume Screening & Candidate Ranking System using NLP

## Project Overview

The Resume Screening & Candidate Ranking System is an AI-powered recruitment assistant developed using Python, Natural Language Processing (NLP), and Machine Learning techniques.

The application allows users to upload multiple resumes and compare them against a job description. It automatically extracts resume content, preprocesses text, calculates similarity scores using TF-IDF and Cosine Similarity, and ranks candidates based on their relevance to the job requirements.

This system helps streamline the recruitment process by reducing manual resume screening efforts and identifying the most suitable candidates efficiently.

---

## Features

- Upload resumes in PDF, DOCX, and TXT formats
- Automatic resume text extraction and parsing
- NLP-based text preprocessing
  - Lowercasing
  - Tokenization
  - Stopword Removal
  - Lemmatization
- TF-IDF Vectorization
- Cosine Similarity Matching
- Skill Extraction and Comparison
- Candidate Ranking based on Match Score
- Identification of Matched and Missing Skills
- Interactive Streamlit Dashboard
- Support for Multiple Resume Uploads

---

## Setup Instructions

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Download NLTK Resources

```bash
python setup_nltk.py
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser.

---

## Usage Details

### Step 1
Launch the application:

```bash
streamlit run app.py
```

### Step 2
Upload one or more resumes in any supported format:

- PDF (.pdf)
- DOCX (.docx)
- TXT (.txt)

### Step 3
Paste the Job Description into the provided text area.

Example:

```text
Python Developer

Required Skills:
Python
Django
SQL
Git
Machine Learning
Docker
AWS
```

### Step 4
Click the **Analyze Candidates** button.

### Step 5
Review the generated results:

- Candidate Match Score (%)
- Ranked Candidate List
- Matched Skills
- Missing Skills
- Top Candidate Recommendation

---

## Technologies Used

- Python
- Streamlit
- NLTK
- Scikit-learn
- Pandas
- pdfplumber
- python-docx

---

## Author

**Harshna Makwana**

