import streamlit as st
import pandas as pd

from parser.pdf_parser import extract_pdf_text
from parser.docx_parser import extract_docx_text
from parser.txt_parser import extract_txt_text

from ranking.similarity import calculate_similarity
from utils.skill_matcher import compare_skills


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# THEME TOKENS (dark mode only)
# --------------------------------------------------

DARK = {
    "bg": "#0B1120",
    "card": "#141B2E",
    "ink": "#F1F5F9",
    "slate": "#94A3B8",
    "mist": "#1E293B",
    "line": "#2A3447",
    "accent": "#818CF8",
    "accent_light": "#272E52",
    "good": "#4ADE80",
    "good_bg": "#0F2818",
    "good_border": "#14532D",
    "bad": "#F87171",
    "bad_bg": "#2A1414",
    "bad_border": "#7F1D1D",
    "sidebar_bg": "#070B14",
    "sidebar_text": "#CBD5E1",
    "banner_bg": "linear-gradient(135deg,#0A2818 0%, #0F2E1B 100%)",
    "banner_border": "#14532D",
    "banner_title": "#86EFAC",
    "banner_sub": "#4ADE80",
    "uploader_border": "#3B3F6B",
    "uploader_bg": "#11162B",
    "shadow": "0 1px 2px rgba(0,0,0,0.3), 0 1px 12px rgba(0,0,0,0.25)",
    "row_hover": "#1A2236",
}

T = DARK


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(f"""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]{{
        font-family:'Inter', sans-serif;
    }}

    :root{{
        --ink:{T['ink']};
        --slate:{T['slate']};
        --mist:{T['mist']};
        --line:{T['line']};
        --accent:{T['accent']};
        --accent-light:{T['accent_light']};
        --good:{T['good']};
        --good-bg:{T['good_bg']};
        --good-border:{T['good_border']};
        --bad:{T['bad']};
        --bad-bg:{T['bad_bg']};
        --bad-border:{T['bad_border']};
        --card:{T['card']};
        --shadow:{T['shadow']};
        --row-hover:{T['row_hover']};
    }}

    .stApp{{
        background:{T['bg']};
    }}

    body, p, span, div, label{{ color:var(--ink); }}

    #MainMenu, footer{{visibility:hidden;}}
    header[data-testid="stHeader"]{{ background:transparent; }}

    .block-container{{
        padding-top:1.6rem;
        max-width:1180px;
    }}

    h1, h2, h3, h4, .hero, .cand-name, .kpi-value{{
        font-family:'Plus Jakarta Sans', sans-serif;
    }}

    /* ---------- Top bar ---------- */
    .top-bar{{
        display:flex;
        justify-content:flex-end;
        margin-bottom:0.6rem;
    }}

    /* ---------- Hero ---------- */
    .hero{{
        background:linear-gradient(135deg,#1E1B4B 0%, #4338CA 60%, #6D28D9 100%);
        border-radius:18px;
        padding:2.4rem 2.6rem;
        margin-bottom:1.6rem;
        color:#fff;
        box-shadow:0 14px 30px -12px rgba(67,56,202,0.5);
    }}
    .hero h1{{
        font-size:1.9rem;
        font-weight:800;
        margin:0 0 0.4rem 0;
        letter-spacing:-0.01em;
        color:#fff;
    }}
    .hero p{{
        font-size:0.98rem;
        color:#E0E7FF;
        margin:0;
        font-weight:400;
        font-family:'Inter', sans-serif;
    }}
    .hero-badge{{
        display:inline-block;
        background:rgba(255,255,255,0.14);
        border:1px solid rgba(255,255,255,0.25);
        padding:0.2rem 0.7rem;
        border-radius:999px;
        font-size:0.72rem;
        font-weight:600;
        letter-spacing:0.04em;
        text-transform:uppercase;
        margin-bottom:0.9rem;
        color:#fff;
        font-family:'Inter', sans-serif;
    }}

    /* ---------- Section labels ---------- */
    .section-label{{
        font-size:0.78rem;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:0.06em;
        color:var(--accent);
        margin-bottom:0.45rem;
        font-family:'Inter', sans-serif;
    }}

    /* ---------- Inputs ---------- */
    textarea{{
        border-radius:10px !important;
        border:1.5px solid var(--line) !important;
        font-size:0.92rem !important;
        background:var(--card) !important;
        color:var(--ink) !important;
    }}
    textarea:focus{{
        border-color:var(--accent) !important;
        box-shadow:0 0 0 3px var(--accent-light) !important;
    }}
    textarea::placeholder{{ color:var(--slate) !important; opacity:0.7; }}

    [data-testid="stFileUploaderDropzone"]{{
        border-radius:10px !important;
        border:1.5px dashed {T['uploader_border']} !important;
        background:{T['uploader_bg']} !important;
    }}
    [data-testid="stFileUploaderDropzone"] *{{ color:var(--ink) !important; }}
    [data-testid="stFileUploaderDropzone"] small{{ color:var(--slate) !important; }}

    /* ---------- Buttons ---------- */
    .stButton > button{{
        background:var(--accent);
        color:#fff;
        border:none;
        border-radius:10px;
        padding:0.65rem 1.6rem;
        font-weight:600;
        font-size:0.95rem;
        letter-spacing:0.01em;
        transition:all 0.15s ease;
        box-shadow:0 4px 12px -4px rgba(67,56,202,0.5);
    }}
    .stButton > button:hover{{
        filter:brightness(1.08);
        box-shadow:0 6px 16px -4px rgba(67,56,202,0.6);
        transform:translateY(-1px);
    }}
    .stButton > button p{{ color:#fff !important; }}

    /* ---------- KPI cards ---------- */
    .kpi-card{{
        background:var(--card);
        border:1px solid var(--line);
        border-radius:14px;
        padding:1.2rem 1.3rem;
        text-align:left;
        height:100%;
        box-shadow:var(--shadow);
    }}
    .kpi-label{{
        font-size:0.76rem;
        color:var(--slate);
        font-weight:600;
        text-transform:uppercase;
        letter-spacing:0.04em;
        margin-bottom:0.3rem;
        font-family:'Inter', sans-serif;
    }}
    .kpi-value{{
        font-size:1.7rem;
        font-weight:700;
        color:var(--ink);
        line-height:1.1;
    }}
    .kpi-value.accent{{ color:var(--accent); }}

    /* ---------- Candidate card ---------- */
    .cand-card{{
        background:var(--card);
        border:1px solid var(--line);
        border-radius:14px;
        padding:1.25rem 1.4rem;
        margin-bottom:0.85rem;
        box-shadow:var(--shadow);
    }}
    .cand-top{{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:0.7rem;
    }}
    .cand-name{{
        font-weight:700;
        font-size:1.02rem;
        color:var(--ink);
    }}
    .rank-pill{{
        display:inline-block;
        background:var(--accent-light);
        color:var(--accent);
        font-weight:700;
        font-size:0.75rem;
        border-radius:999px;
        padding:0.15rem 0.6rem;
        margin-right:0.55rem;
        font-family:'Inter', sans-serif;
    }}
    .score-text{{
        font-weight:700;
        font-size:0.95rem;
    }}

    .bar-track{{
        background:var(--mist);
        border-radius:999px;
        height:8px;
        width:100%;
        overflow:hidden;
        margin-bottom:0.85rem;
    }}
    .bar-fill{{
        height:100%;
        border-radius:999px;
    }}

    .skill-badge{{
        display:inline-block;
        font-size:0.76rem;
        font-weight:600;
        padding:0.22rem 0.65rem;
        border-radius:999px;
        margin:0.15rem 0.3rem 0.15rem 0;
        font-family:'Inter', sans-serif;
    }}
    .skill-good{{
        background:var(--good-bg);
        color:var(--good);
        border:1px solid var(--good-border);
    }}
    .skill-bad{{
        background:var(--bad-bg);
        color:var(--bad);
        border:1px solid var(--bad-border);
    }}
    .skill-group-label{{
        font-size:0.72rem;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:0.04em;
        color:var(--slate);
        margin:0.5rem 0 0.3rem 0;
        font-family:'Inter', sans-serif;
    }}
    .skill-none{{ color:var(--slate); font-size:0.85rem; }}

    /* ---------- Top banner ---------- */
    .top-banner{{
        background:{T['banner_bg']};
        border:1px solid {T['banner_border']};
        border-radius:14px;
        padding:1.1rem 1.4rem;
        margin:1rem 0 1.4rem 0;
        display:flex;
        align-items:center;
        gap:0.8rem;
    }}
    .top-banner .icon{{ font-size:1.6rem; }}
    .top-banner .msg-title{{
        font-weight:700;
        color:{T['banner_title']};
        font-size:0.98rem;
        font-family:'Plus Jakarta Sans', sans-serif;
    }}
    .top-banner .msg-sub{{
        color:{T['banner_sub']};
        font-size:0.85rem;
    }}

    /* ---------- Custom ranking table ---------- */
    .rank-table{{
        background:var(--card);
        border:1px solid var(--line);
        border-radius:14px;
        overflow:hidden;
        box-shadow:var(--shadow);
    }}
    .rank-table-head{{
        display:grid;
        grid-template-columns:50px 1.6fr 1fr 90px;
        gap:0.8rem;
        padding:0.7rem 1.2rem;
        font-size:0.72rem;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:0.05em;
        color:var(--slate);
        border-bottom:1px solid var(--line);
        font-family:'Inter', sans-serif;
    }}
    .rank-table-row{{
        display:grid;
        grid-template-columns:50px 1.6fr 1fr 90px;
        gap:0.8rem;
        align-items:center;
        padding:0.85rem 1.2rem;
        border-bottom:1px solid var(--line);
        transition:background 0.12s ease;
    }}
    .rank-table-row:last-child{{ border-bottom:none; }}
    .rank-table-row:hover{{ background:var(--row-hover); }}
    .rt-rank{{
        font-weight:700;
        color:var(--slate);
        font-size:0.9rem;
    }}
    .rt-name{{
        font-weight:600;
        color:var(--ink);
        font-size:0.92rem;
        overflow:hidden;
        text-overflow:ellipsis;
        white-space:nowrap;
    }}
    .rt-score-val{{
        font-weight:700;
        font-size:0.85rem;
        margin-bottom:0.25rem;
    }}
    .rt-skills{{
        text-align:right;
        font-size:0.85rem;
        color:var(--slate);
        font-weight:600;
    }}

    hr{{ border-color:var(--line) !important; }}

    [data-testid="stSidebar"]{{
        background:{T['sidebar_bg']};
    }}
    [data-testid="stSidebar"] *{{
        color:{T['sidebar_text']} !important;
    }}
    [data-testid="stSidebar"] h3{{
        color:#fff !important;
        font-family:'Plus Jakarta Sans', sans-serif;
    }}

    [data-testid="stAlert"]{{
        background:var(--card);
        border:1px solid var(--line);
        border-radius:10px;
    }}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("### 📄 Resume Screener")
    st.markdown(
        "An NLP-powered tool that ranks candidates against a job "
        "description using semantic similarity and skill matching."
    )
    st.markdown("---")
    st.markdown("#### How it works")
    st.markdown(
        "1. Paste the job description\n"
        "2. Upload two or more resumes\n"
        "3. Click **Analyze Candidates**\n"
        "4. Review ranked results and skill gaps"
    )
    st.markdown("---")
    st.markdown("#### Supported formats")
    st.markdown("`.pdf`  ·  `.docx`  ·  `.txt`")
    st.markdown("---")
    st.caption("Built with Streamlit · NLP similarity scoring")


# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------

st.markdown(
    '<div class="hero">'
    '<div class="hero-badge">AI-Powered · NLP Resume Analysis</div>'
    '<h1>Resume Screening & Candidate Ranking</h1>'
    '<p>Paste a job description, upload resumes, and instantly rank candidates by relevance and skill fit.</p>'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# JOB DESCRIPTION + FILE UPLOAD
# --------------------------------------------------

MIN_RESUMES = 2

col_left, col_right = st.columns([1.15, 1], gap="large")

with col_left:
    st.markdown('<div class="section-label">Step 1 — Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        " ",
        height=230,
        placeholder="Paste the full job description here (responsibilities, required skills, qualifications)...",
        label_visibility="collapsed"
    )

with col_right:
    st.markdown('<div class="section-label">Step 2 — Upload Resumes</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        " ",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help=f"Upload at least {MIN_RESUMES} resumes to compare candidates."
    )

    if uploaded_files:
        if len(uploaded_files) < MIN_RESUMES:
            st.caption(f"⚠️ {len(uploaded_files)} file uploaded — add at least {MIN_RESUMES} to compare candidates")
        else:
            st.caption(f"✅ {len(uploaded_files)} file(s) ready for analysis")
    else:
        st.caption(f"No files uploaded yet — upload at least {MIN_RESUMES} resumes")

st.write("")
analyze_clicked = st.button("🔍 Analyze Candidates", use_container_width=False)
st.markdown("---")


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def score_color(score: float) -> str:
    if score >= 75:
        return T["good"]
    elif score >= 50:
        return "#FBBF24"
    else:
        return T["bad"]


def render_skill_badges(skills_str: str, kind: str) -> str:
    skills = [s.strip() for s in skills_str.split(",") if s.strip()]
    if not skills:
        return '<span class="skill-none">None</span>'
    css_class = "skill-good" if kind == "good" else "skill-bad"
    return "".join(f'<span class="skill-badge {css_class}">{s}</span>' for s in skills)


def render_ranking_table(df: pd.DataFrame) -> str:
    rows_html = ""
    for i, row in df.iterrows():
        rank = i + 1
        score = row["Match Score (%)"]
        color = score_color(score)
        rows_html += (
            '<div class="rank-table-row">'
            f'<div class="rt-rank">#{rank}</div>'
            f'<div class="rt-name" title="{row["Candidate"]}">{row["Candidate"]}</div>'
            '<div>'
            f'<div class="rt-score-val" style="color:{color};">{score}%</div>'
            '<div class="bar-track" style="margin-bottom:0;">'
            f'<div class="bar-fill" style="width:{score}%; background:{color};"></div>'
            '</div>'
            '</div>'
            f'<div class="rt-skills">{row["Matched Count"]} matched</div>'
            '</div>'
        )

    return (
        '<div class="rank-table">'
        '<div class="rank-table-head">'
        '<div>Rank</div><div>Candidate</div><div>Match Score</div>'
        '<div style="text-align:right;">Skills</div>'
        '</div>'
        f'{rows_html}'
        '</div>'
    )


# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

if analyze_clicked:

    if not job_description:
        st.warning("⚠️ Please enter a job description before analyzing.")
        st.stop()

    if not uploaded_files:
        st.warning("⚠️ Please upload at least one resume.")
        st.stop()

    if len(uploaded_files) < MIN_RESUMES:
        st.warning(f"⚠️ Please upload at least {MIN_RESUMES} resumes so candidates can be compared.")
        st.stop()

    results = []

    with st.spinner("Analyzing resumes..."):

        for file in uploaded_files:

            filename = file.name

            try:
                # ------------------------------
                # PARSE FILE
                # ------------------------------

                if filename.endswith(".pdf"):
                    resume_text = extract_pdf_text(file)

                elif filename.endswith(".docx"):
                    resume_text = extract_docx_text(file)

                elif filename.endswith(".txt"):
                    resume_text = extract_txt_text(file)

                else:
                    continue

                # ------------------------------
                # SIMILARITY SCORE
                # ------------------------------

                score = calculate_similarity(
                    job_description,
                    resume_text
                )

                # ------------------------------
                # SKILL MATCHING
                # ------------------------------

                matched_skills, missing_skills = compare_skills(
                    job_description,
                    resume_text
                )

                results.append({
                    "Candidate": filename,
                    "Match Score (%)": score,
                    "Matched Skills": ", ".join(matched_skills),
                    "Missing Skills": ", ".join(missing_skills),
                    "Matched Count": len(matched_skills)
                })

            except Exception as e:
                st.error(f"Error processing {filename}: {e}")

    if not results:
        st.error("No resumes could be processed. Please check the uploaded files.")
        st.stop()

    # --------------------------------------------------
    # SORT RESULTS
    # --------------------------------------------------

    results = sorted(
        results,
        key=lambda x: x["Match Score (%)"],
        reverse=True
    )

    df = pd.DataFrame(results)
    top_candidate = df.iloc[0]

    # --------------------------------------------------
    # TOP CANDIDATE BANNER
    # --------------------------------------------------

    st.markdown(
        '<div class="top-banner">'
        '<div class="icon">🏆</div>'
        '<div>'
        f'<div class="msg-title">Top Candidate: {top_candidate["Candidate"]}</div>'
        f'<div class="msg-sub">Match Score {top_candidate["Match Score (%)"]}% · {top_candidate["Matched Count"]} skills matched</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # DASHBOARD METRICS
    # --------------------------------------------------

    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4, gap="medium")

    avg_score = round(df["Match Score (%)"].mean(), 1)

    with k1:
        st.markdown(
            '<div class="kpi-card">'
            '<div class="kpi-label">Total Resumes</div>'
            f'<div class="kpi-value">{len(df)}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with k2:
        st.markdown(
            '<div class="kpi-card">'
            '<div class="kpi-label">Top Score</div>'
            f'<div class="kpi-value accent">{top_candidate["Match Score (%)"]}%</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with k3:
        st.markdown(
            '<div class="kpi-card">'
            '<div class="kpi-label">Average Score</div>'
            f'<div class="kpi-value">{avg_score}%</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with k4:
        st.markdown(
            '<div class="kpi-card">'
            '<div class="kpi-label">Best Candidate</div>'
            f'<div class="kpi-value" style="font-size:1.1rem; word-break:break-word;">{top_candidate["Candidate"]}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.write("")
    st.markdown("---")

    # --------------------------------------------------
    # RANKING TABLE (theme-aware custom HTML)
    # --------------------------------------------------

    st.markdown('<div class="section-label">Candidate Rankings</div>', unsafe_allow_html=True)
    st.markdown(render_ranking_table(df), unsafe_allow_html=True)

    st.write("")
    st.markdown("---")

    # --------------------------------------------------
    # DETAILED CANDIDATE CARDS
    # --------------------------------------------------

    st.markdown('<div class="section-label">Detailed Breakdown</div>', unsafe_allow_html=True)

    for i, row in df.iterrows():
        rank = i + 1
        color = score_color(row["Match Score (%)"])

        card_html = (
            '<div class="cand-card">'
            '<div class="cand-top">'
            '<div>'
            f'<span class="rank-pill">#{rank}</span>'
            f'<span class="cand-name">{row["Candidate"]}</span>'
            '</div>'
            f'<span class="score-text" style="color:{color};">{row["Match Score (%)"]}%</span>'
            '</div>'
            '<div class="bar-track">'
            f'<div class="bar-fill" style="width:{row["Match Score (%)"]}%; background:{color};"></div>'
            '</div>'
            '<div class="skill-group-label">✅ Matched Skills</div>'
            f'<div>{render_skill_badges(row["Matched Skills"], "good")}</div>'
            '<div class="skill-group-label">❌ Missing Skills</div>'
            f'<div>{render_skill_badges(row["Missing Skills"], "bad")}</div>'
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

else:
    st.info("👆 Enter a job description and upload resumes, then click **Analyze Candidates** to see results.")