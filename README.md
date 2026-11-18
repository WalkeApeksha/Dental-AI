# Dental Assignment Analyzer

A research data-analysis project for **Mini-Project 1** of the Mitacs research project
**"AI in Dental Education, Access to Care, and Reflective Provider."**

This tool analyses assignments submitted by undergraduate dental students and identifies
what students **understand, believe, and communicate** about three important public
dental-health issues.

---

## Table of Contents

1. [What This Project Does](#what-this-project-does)
2. [The Three Assignment Topics](#the-three-assignment-topics)
3. [Project Workflow](#project-workflow)
4. [Tech Stack & Role of Each Tool](#tech-stack--role-of-each-tool)
5. [Project Structure](#project-structure)
6. [Prerequisites](#prerequisites)
7. [Installation & Setup](#installation--setup)
8. [How to Run](#how-to-run)
9. [Quick-Start Checklist](#quick-start-checklist)
10. [Troubleshooting](#troubleshooting)
11. [Outputs](#outputs)
12. [Thematic Coding Framework](#thematic-coding-framework)
13. [Limitations](#limitations)
14. [Author & Acknowledgements](#author--acknowledgements)

---

## What This Project Does

The Dental Assignment Analyzer automates the research workflow for analysing dental
student assignments. It performs:

- **Text extraction** from PDF, DOCX, and TXT assignment files
- **Data cleaning & anonymization** (removes names, emails, student IDs; de-duplicates)
- **Topic classification** into three assignment topics
- **Thematic analysis** using a keyword-based coding framework (7 themes)
- **Quantitative analysis** (counts, percentages, word counts)
- **Sentiment coding** (positive / negative / neutral)
- **Comparative analysis** across the three topics
- **Visualization** (bar charts, pie chart) and **report generation**
- **Interactive web dashboard** for exploring the results

The goal is a combination of **manual thematic analysis + Python-based quantitative
analysis**, as recommended for a research internship of this scope.

---

## The Three Assignment Topics

### 1. Community Water Fluoridation
Students' understanding of adding fluoride to community water supplies to prevent tooth decay.
Focus areas: benefits, possible risks, public health perspectives, personal arguments.

### 2. Universal Access to Dental Care
Students' views on ensuring everyone can access affordable dental treatment.
Focus areas: affordability, rural/underserved communities, healthcare inequality,
government policy and advocacy.

### 3. Sugary Beverage Vending Machines in Elementary Schools
Students' opinions on selling sugary drinks in elementary schools.
Focus areas: effects of sugar on oral health, childhood cavities, school health policy,
healthy beverage alternatives.

---

## Project Workflow

The project follows the six research modules described in the brief:

| Module | Description | Implemented in |
|--------|-------------|----------------|
| 1. Data collection | Collect student assignments (PDF/DOCX/TXT) | `data/raw/` |
| 2. Data preprocessing | Extract text, clean, anonymize, de-duplicate | `analyze.py` |
| 3. Thematic analysis | Identify recurring themes via coding framework | `analyze.py` |
| 4. Quantitative analysis | Counts, percentages, sentiment distribution | `analyze.py` |
| 5. Comparative analysis | Compare themes and sentiment across topics | `analyze.py` + `app.py` |
| 6. Report & visualization | Charts, tables, summary report, dashboard | `analyze.py` + `app.py` |

---

## Tech Stack & Role of Each Tool

| Technology | Role in This Project | Why It Was Chosen |
|------------|----------------------|-------------------|
| **Python 3** | Main programming language for the entire analysis pipeline | Readable, huge ecosystem for text analysis, standard in research |
| **Pandas** | Data processing — loads assignments into a DataFrame, groups by topic, computes counts and percentages, exports CSV | Handles tabular data and aggregation cleanly with minimal code |
| **python-docx** | Extracts text from `.docx` assignment submissions | Most students submit Word documents; this reads paragraph text directly |
| **PyPDF2** | Extracts text from `.pdf` assignment submissions | Many assignments arrive as PDFs; this pulls text page by page |
| **re (regex)** | Cleans whitespace/control characters and **anonymizes** names, emails, and student IDs | Fast, built-in pattern matching — no extra dependency for anonymization |
| **Matplotlib** | Generates static PNG charts (topics, themes, sentiment) saved to `data/output/` | Reliable headless chart generation (`Agg` backend) for reports |
| **Streamlit** | Builds the interactive web dashboard (`app.py`) to explore results | Turns a Python script into a web app in minutes — no HTML/CSS/JS needed |
| **OpenPyXL** | (Optional) Supports Excel export via Pandas | Needed if you export `.xlsx` instead of CSV |
| **Virtual environment (venv)** | Isolates project dependencies | Prevents version conflicts with other projects on the machine |

> **Note on optional tools:** The recommended stack also lists NLTK/spaCy (NLP),
> Scikit-learn (classification/clustering), and SQLite (storage). For a mini-project
> of this size, keyword-based thematic coding covers the research needs. Those tools
> can be added later for automated NLP or ML-based topic clustering if the supervisor
> requests it.

---

## Project Structure

```
Dental/
├── .venv/                     # Python virtual environment
├── data/
│   ├── raw/                   # Input: student assignments (.txt / .docx / .pdf)
│   └── output/                # Generated: CSV, PNG charts, summary report
├── analyze.py                 # Main analysis pipeline
├── app.py                     # Streamlit dashboard
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

---

## Prerequisites

Before you begin, make sure you have:

- **Python 3.9 or newer** installed — check with `python --version`
- **pip** available — check with `pip --version`
- **VS Code** (recommended editor) with the Python extension
- **PowerShell** (Windows) or Terminal (macOS/Linux)
- **Internet access** for the one-time package installation

> If `python` is not recognized, install Python from <https://www.python.org/downloads/>
> and tick **"Add Python to PATH"** during installation.

---

## Installation & Setup

### Step 1 — Open the project folder

```powershell
cd C:\Users\yashs\OneDrive\Desktop\Dental
```

### Step 2 — Create a virtual environment

```powershell
python -m venv .venv
```

### Step 3 — Activate the virtual environment

**Windows PowerShell:**
```powershell
.venv\Scripts\activate
```

If you see an error like `running scripts is disabled on this system`, run this once
in the same window, then retry activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate
```

**Windows Command Prompt (alternative):**
```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

After activation, your prompt should start with `(.venv)`.

### Step 4 — Install the required dependencies

Copy and run this single command:

```powershell
pip install pandas numpy matplotlib python-docx PyPDF2 streamlit openpyxl
```

**What each dependency is for:**

| Package | Purpose |
|---------|---------|
| `pandas` | Data processing, grouping, statistics, CSV export |
| `numpy` | Numerical support used by pandas/matplotlib |
| `matplotlib` | Generating PNG charts |
| `python-docx` | Reading `.docx` assignments |
| `PyPDF2` | Reading `.pdf` assignments |
| `streamlit` | Interactive web dashboard |
| `openpyxl` | Excel export support (optional but recommended) |

> **Optional extras** (only needed if you later add NLP or ML): `nltk`, `spacy`,
> `scikit-learn`, `plotly`. Install with:
> ```powershell
> pip install nltk spacy scikit-learn plotly
> python -m spacy download en_core_web_sm
> ```

### Step 5 — (Recommended) Freeze dependencies

```powershell
pip freeze > requirements.txt
```

This writes the exact installed versions into `requirements.txt`. On another machine,
you can then install everything with:

```powershell
pip install -r requirements.txt
```

---

## How to Run

### Step 1 — Add the assignment files

Place student assignments into the **`data/raw/`** folder.
Supported formats: **`.txt`**, **`.docx`**, **`.pdf`**.

> Sample `.txt` files are already included so you can test the pipeline immediately.

### Step 2 — Run the analysis pipeline

```powershell
python analyze.py
```

This will:
- Extract text from every file in `data/raw/`
- Clean and anonymize the text
- Classify each assignment by topic
- Tag themes and sentiment
- Save `assignments_analyzed.csv`, three charts, and `summary_report.txt` into `data/output/`

Expected terminal output looks like:

```
Analyzed 5 assignments -> ...\data\output\assignments_analyzed.csv

Topic distribution:
fluoridation    2
vending         2
access          1

Sentiment:
positive    4
neutral     1

Theme frequency:
prevention          8
...
Charts + report -> ...\data\output
```

### Step 3 — Launch the interactive dashboard

```powershell
streamlit run app.py
```

Streamlit will print a local URL (usually **http://localhost:8501**) and open it in
your browser automatically. Press `Ctrl + C` in the terminal to stop the server.

The dashboard shows:
- KPI cards (assignments, themes, topics, average word count)
- Bar charts for topics and sentiment
- Theme frequency chart
- Comparative theme-by-topic chart
- Anonymized data table
- Sidebar topic filter + download buttons for CSV and report

### Step 4 — Re-run after adding new assignments

Whenever new assignments are added to `data/raw/`, simply re-run:

```powershell
python analyze.py
```

Then refresh the browser tab running the dashboard (or restart `streamlit run app.py`).

---

## Quick-Start Checklist

Copy-paste this block into PowerShell from the project root to set up and run everything
in one go:

```powershell
# 1. Create + activate venv
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate

# 2. Install dependencies
pip install pandas numpy matplotlib python-docx PyPDF2 streamlit openpyxl

# 3. Save dependency list
pip freeze > requirements.txt

# 4. Run the analysis
python analyze.py

# 5. Launch the dashboard
streamlit run app.py
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `running scripts is disabled on this system` | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then reactivate |
| `python` is not recognized | Reinstall Python with "Add to PATH", or use `py` instead of `python` |
| `ModuleNotFoundError: No module named 'pandas'` | The venv is not activated, or `pip install` was run outside it. Activate and reinstall |
| Streamlit says "No data found" | Run `python analyze.py` first so the CSV exists in `data/output/` |
| Chart file not generated on a headless machine | Already handled — `matplotlib.use("Agg")` is set in `analyze.py` |
| PDF text extraction returns empty | Some scanned PDFs need OCR; convert to text or use a digital PDF |
| Duplicate assignments still appear | Duplicate detection uses a hash of the cleaned text; near-duplicates with edits are treated as different |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |

---

## Outputs

After running `analyze.py`, the `data/output/` folder contains:

| File | Description |
|------|-------------|
| `assignments_analyzed.csv` | Cleaned, anonymized dataset with topic, sentiment, word count, and theme counts |
| `chart_topics.png` | Bar chart: number of assignments per topic |
| `chart_themes.png` | Bar chart: theme frequency across all assignments |
| `chart_sentiment.png` | Pie chart: sentiment distribution |
| `summary_report.txt` | Text summary of all statistics |

The Streamlit dashboard additionally shows KPI cards, a comparative theme-by-topic
chart, an interactive data table, topic filters, and download buttons.

---

## Thematic Coding Framework

Seven themes are coded using keyword matching:

| Theme | Example Keywords |
|-------|------------------|
| Public health | public health, population, community |
| Healthcare equality | equality, inequality, equity, disparity |
| Preventive dentistry | prevent, prevention, cavities, decay |
| Government responsibility | government, policy, legislation, advocacy |
| Personal opinion | I believe, I think, in my opinion, I feel |
| Cost / affordability | cost, afford, expensive, financial |
| Risk / concern | risk, concern, danger, harm, side effect |

**Sentiment coding:**
- **Positive** keywords: benefit, effective, safe, improve, reduce, good, important, support
- **Negative** keywords: risk, harm, danger, concern, inequality, barrier, cost, bad

> This framework should be reviewed and refined with the Mitacs supervisor to ensure
> coding consistency with manual thematic analysis.

---

## Limitations

- **Keyword-based coding** may miss paraphrased or implicit themes; manual review of
  sampled assignments is recommended to validate coding accuracy.
- **Sentiment analysis** is lexicon-based (keyword counting), not a trained model —
  it captures overall tone but not nuance or sarcasm.
- **Topic classification** assumes each assignment addresses a single topic; assignments
  covering multiple topics are assigned to the dominant one.
- **Anonymization** uses pattern matching and may not catch every name format.
- Results depend on the **quality and quantity** of assignments provided by the supervisor.

---

## Author & Acknowledgements

Built as part of **Mini-Project 1** under the Mitacs research project
**"AI in Dental Education, Access to Care, and Reflective Provider."**

**Author:** Yash [Last Name]
**Supervisor:** [Mitacs Supervisor Name]
**Institution:** [Your University / Institution]