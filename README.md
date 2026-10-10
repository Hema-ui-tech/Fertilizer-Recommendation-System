# Candidate Performance Analysis & Recommendation Tool

A simple AI/ML-style web app built with **Python + Streamlit** that implements the
Wipro Talent Next "Candidate Performance Analysis & Recommendation Tool" requirements.

## What it does (mapped to requirements)

| ID | Requirement | Where it's implemented |
|----|-------------|--------------------------|
| ANAR1 | Read performance report from CSV/Excel | `logic.load_data()` |
| ANAR2 | Highlight Strength/Weakness of candidates | `logic.candidate_summary()` |
| ANAR3 | Recommend To-Do course list for weak performers | `logic.recommend_courses()` |
| ANAR4 | Find poor performers, pair with good performers | `logic.pair_students()` |
| ANAR5 | Highlight who is improving across attempts | `logic.improvement_tracking()` |
| ANAR6 | Dashboard with overall class performance | Dashboard tab in `app.py` |
| ANAR7 | Deployable as a web component | Entire app runs as a Streamlit web app |

## Project files

```
candidate_perf_tool/
├── app.py               # Streamlit UI (the web app)
├── logic.py             # Data processing & recommendation engine (reusable/testable)
├── sample_dataset.csv    # 100 synthetic students x 5 courses x multiple attempts
├── requirements.txt
└── README.md
```

## How to run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501) and upload
`sample_dataset.csv` (or your own file with the same columns) from the sidebar.

## Expected input format

Your CSV/Excel file must contain these columns (any extra columns are ignored):

```
Course Name, Course ID, Attempt ID, Candidate Name, Candidate Email, Mark, Grade
```

A student can appear multiple times per course (different `Attempt ID`s) if they
retook a test — the tool automatically uses the **best attempt** for the
strength/weakness report, and uses **first vs. latest attempt** to detect improvement.

## Customizing the logic

Open `logic.py` and adjust:
- `POOR_MAX` / `MEDIUM_MAX` — score thresholds for Poor / Medium / High bands.
- `TODO_COURSES` — the recommended course list shown for each performance band.
- `pair_students()` — mentor/mentee pairing strategy (currently simple round-robin).

## Deploying online (optional, free)

1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Point it at `app.py` in your repo — it will build and give you a public URL.

This satisfies the "deployable as a web component" (ANAR7) requirement without
needing any server management.
