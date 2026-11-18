"""
Dental Student Assignments - Simple Analysis
Run: python analyze.py
"""

import re
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from PyPDF2 import PdfReader

ROOT = Path(__file__).parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "output"
OUT.mkdir(parents=True, exist_ok=True)

TOPICS = {
    "fluoridation": ["fluorid", "water fluoridation"],
    "access": ["access to care", "affordab", "underserved", "rural", "inequal"],
    "vending": ["vending", "sugary", "soda", "elementary school"],
}

THEMES = {
    "public_health": ["public health", "population", "community"],
    "equality": ["equality", "inequality", "equity", "disparit"],
    "prevention": ["prevent", "prevention", "cavities", "decay"],
    "government": ["government", "policy", "polic", "legislat", "advocacy"],
    "personal_opinion": ["i believe", "i think", "in my opinion", "i feel"],
    "cost": ["cost", "afford", "expensive", "financial"],
    "risk": ["risk", "concern", "danger", "harm", "side effect"],
}

POSITIVE = ["benefit", "effective", "safe", "improve", "reduce", "good", "important", "support"]
NEGATIVE = ["risk", "harm", "danger", "concern", "inequality", "barrier", "cost", "bad"]


def extract(path):
    ext = path.suffix.lower()
    if ext == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if ext == ".docx":
        return "\n".join(p.text for p in Document(str(path)).paragraphs)
    if ext == ".pdf":
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(path)).pages)
    return ""


def clean_anon(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", "[EMAIL]", text)
    text = re.sub(r"\b[A-Z]?\d{6,10}\b", "[ID]", text)
    text = re.sub(r"(?i)(name|student)\s*[:\-]\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",
                  r"\1: [NAME]", text)
    return text


def count_hits(text, keywords):
    t = text.lower()
    return sum(t.count(k) for k in keywords)


def classify_topic(text):
    scores = {tp: count_hits(text, kws) for tp, kws in TOPICS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unclassified"


def sentiment(text):
    pos = count_hits(text, POSITIVE)
    neg = count_hits(text, NEGATIVE)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def main():
    rows = []
    files = [p for p in RAW.glob("*") if p.suffix.lower() in {".txt", ".docx", ".pdf"}]
    if not files:
        print(f"No files in {RAW}. Add assignments first.")
        return

    seen = set()
    for p in files:
        raw = extract(p)
        if not raw.strip():
            continue
        text = clean_anon(raw)
        h = hash(text)
        if h in seen:
            continue
        seen.add(h)

        row = {
            "file": p.name,
            "topic": classify_topic(text),
            "sentiment": sentiment(text),
            "word_count": len(text.split()),
            "text": text,
        }
        for theme, kws in THEMES.items():
            row[theme] = count_hits(text, kws)
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "assignments_analyzed.csv", index=False)
    print(f"Analyzed {len(df)} assignments -> {OUT / 'assignments_analyzed.csv'}")

    topic_counts = df["topic"].value_counts()
    sentiment_counts = df["sentiment"].value_counts()
    theme_totals = df[list(THEMES)].sum().sort_values(ascending=False)

    print("\nTopic distribution:\n", topic_counts.to_string())
    print("\nSentiment:\n", sentiment_counts.to_string())
    print("\nTheme frequency:\n", theme_totals.to_string())

    plt.figure()
    topic_counts.plot(kind="bar", color="#4c9aff")
    plt.title("Assignments per Topic")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(OUT / "chart_topics.png")
    plt.close()

    plt.figure()
    theme_totals.plot(kind="barh", color="#38b2ac")
    plt.title("Theme Frequency (all assignments)")
    plt.xlabel("Mentions")
    plt.tight_layout()
    plt.savefig(OUT / "chart_themes.png")
    plt.close()

    plt.figure()
    sentiment_counts.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Sentiment Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUT / "chart_sentiment.png")
    plt.close()

    with open(OUT / "summary_report.txt", "w", encoding="utf-8") as f:
        f.write("DENTAL ASSIGNMENT ANALYSIS - SUMMARY\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Assignments analyzed: {len(df)}\n\n")
        f.write("Topic distribution:\n" + topic_counts.to_string() + "\n\n")
        f.write("Sentiment distribution:\n" + sentiment_counts.to_string() + "\n\n")
        f.write("Theme frequency:\n" + theme_totals.to_string() + "\n")
    print(f"\nCharts + report -> {OUT}")


if __name__ == "__main__":
    main()
