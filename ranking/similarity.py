from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(job_description, resume_text):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [job_description, resume_text]
    )

    similarity_score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )

    return round(
        similarity_score[0][0] * 100,
        2
    )