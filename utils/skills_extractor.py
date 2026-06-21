SKILLS = [
    "python",
    "django",
    "flask",
    "sql",
    "mysql",
    "postgresql",
    "java",
    "javascript",
    "react",
    "html",
    "css",
    "git",
    "docker",
    "aws",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pandas",
    "numpy"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return found_skills