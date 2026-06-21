from ranking.candidate_ranker import rank_candidates

job_description = """
Looking for a Python Developer.

Required Skills:

Python
Django
SQL
Git
Machine Learning
"""

results = rank_candidates(
    job_description,
    "resumes/ENGINEERING"
)

for rank, candidate in enumerate(results[:10], start=1):
    print(
        f"{rank}. {candidate['name']} - {candidate['score']}%"
    )