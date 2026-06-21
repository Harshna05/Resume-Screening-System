# Resume Screening & Candidate Ranking System using NLP

An AI-powered recruitment assistant that parses resumes and ranks candidates against a job description using Natural Language Processing (NLP).

---

## Project Overview

The Resume Screening & Candidate Ranking System automates the process of resume evaluation by comparing candidate resumes with a given job description.

The application extracts text from resumes, preprocesses the content using NLP techniques, calculates similarity scores using TF-IDF and Cosine Similarity, and ranks candidates based on their relevance to the job requirements.

The system also identifies matched and missing skills, helping recruiters make faster and more informed hiring decisions.

---
## Repository Information

**Important:** The latest stable version of this project is maintained in the **master** branch.

After cloning the repository, switch to the master branch using:

```bash
git checkout master
```

## Features

### Resume Parsing
- Supports PDF resumes using pdfplumber
- Supports DOCX resumes using python-docx
- Supports TXT resumes

### Text Preprocessing
- Lowercasing
- Tokenization
- Stopword Removal
- Lemmatization

### Similarity Matching
- TF-IDF Vectorization
- Cosine Similarity Scoring
- Resume-to-Job Description Matching

### Candidate Ranking
- Match Percentage Calculation
- Ranked Candidate List
- Top Candidate Recommendation

### Skill Analysis
- Skill Extraction
- Matched Skills Detection
- Missing Skills Identification

### User Interface
- Built using Streamlit
- Multiple Resume Upload Support
- Interactive Dashboard
- Real-Time Candidate Ranking

---

## Project Structure

```text
Resume Screening System
│
├── app.py
├── setup_nltk.py
├── requirements.txt
├── README.md
│
├── parser
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── txt_parser.py
│
├── preprocessing
│   └── text_cleaner.py
│
├── ranking
│   └── similarity.py
│
├── utils
│   ├── skills_extractor.py
│   └── skill_matcher.py
│
├── resumes
│
├── test_parser.py
├── test_cleaner.py
├── test_similarity.py
├── test_skills.py
├── test_skill_matching.py
└── test_ranking.py
```

---

## Prerequisites

- Python 3.10 or above
- pip
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Resume-Screening-System
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Download NLTK Resources

```bash
python setup_nltk.py
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser.

---

## Usage

### Step 1
Launch the application:

```bash
streamlit run app.py
```

### Step 2
Upload one or more resumes in:

- PDF (.pdf)
- DOCX (.docx)
- TXT (.txt)

### Step 3
Paste the Job Description into the text area.

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
Click **Analyze Candidates**.

### Step 5
View:
- Candidate Rankings
- Match Scores
- Matched Skills
- Missing Skills
- Best Candidate Recommendation

---

## Sample Output

| Rank | Candidate | Match Score |
|------|------------|-------------|
| 1 | Candidate A | 89% |
| 2 | Candidate B | 82% |
| 3 | Candidate C | 75% |

---

## Future Improvements

- Advanced Skill Matching
- Semantic Similarity using Sentence Transformers
- Resume Export Reports
- Candidate Recommendation Dashboard
- Cloud Deployment

---

## Author

**Harshna Makwana**
