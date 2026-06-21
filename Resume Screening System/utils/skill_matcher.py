from utils.skills_extractor import extract_skills


def compare_skills(job_description, resume_text):

    job_skills = set(
        extract_skills(job_description)
    )

    resume_skills = set(
        extract_skills(resume_text)
    )

    matched = list(
        job_skills.intersection(resume_skills)
    )

    missing = list(
        job_skills - resume_skills
    )

    return matched, missing