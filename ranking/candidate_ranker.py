import os

from parser.pdf_parser import extract_pdf_text
from preprocessing.text_cleaner import preprocess_text
from ranking.similarity import calculate_similarity
from utils.skill_matcher import compare_skills


def rank_candidates(job_description, resumes_folder):

    results = []

    clean_job = preprocess_text(job_description)

    for root, dirs, files in os.walk(resumes_folder):

        for file in files:

            if file.lower().endswith(".pdf"):

                file_path = os.path.join(root, file)

                try:

                    resume_text = extract_pdf_text(file_path)

                    clean_resume = preprocess_text(resume_text)

                    score = calculate_similarity(
                        clean_job,
                        clean_resume
                    )

                    matched, missing = compare_skills(
                        job_description,
                        resume_text
                    )

                    results.append({
                        "name": file,
                        "score": score,
                        "matched": matched,
                        "missing": missing
                    })

                except Exception as e:

                    print(f"Error processing {file}: {e}")

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results