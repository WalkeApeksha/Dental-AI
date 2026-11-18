import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "data" / "output"
CSV = OUT / "assignments_analyzed.csv"

st.set_page_config(page_title="Dental Assignment Analyzer", layout="wide")

st.title("Dental Assignment Analyzer")
st.caption("Mini-Project 1 — AI in Dental Education (Mitacs)")

if not CSV.exists():
    st.error(f"No data found at {CSV}. Run `python analyze.py` first.")
    st.stop()

df = pd.read_csv(CSV)

# ---------- KPI row ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Assignments analyzed", len(df))
c2.metric("Themes identified", 7)
c3.metric("Assignment topics", df["topic"].nunique())
c4.metric("Avg. words / assignment", int(df["word_count"].mean()))

st.divider()

# ---------- Charts ----------
left, right = st.columns(2)

with left:
    st.subheader("Assignments per Topic")
    topic_counts = df["topic"].value_counts()
    st.bar_chart(topic_counts)

with right:
    st.subheader("Sentiment Distribution")
    sent_counts = df["sentiment"].value_counts()
    st.bar_chart(sent_counts)

st.divider()

# ---------- Theme frequency ----------
st.subheader("Theme Frequency (all assignments)")
theme_cols = ["public_health", "equality", "prevention", "government",
              "personal_opinion", "cost", "risk"]
theme_totals = df[theme_cols].sum().sort_values(ascending=False)
st.bar_chart(theme_totals)

st.divider()

# ---------- Theme by topic (comparative) ----------
st.subheader("Theme Frequency by Topic")
theme_by_topic = df.groupby("topic")[theme_cols].sum().T
st.bar_chart(theme_by_topic)

st.divider()

# ---------- Data table ----------
st.subheader("Anonymized Assignment Data")
show_cols = ["file", "topic", "sentiment", "word_count"] + theme_cols
st.dataframe(df[show_cols], use_container_width=True)

# ---------- Filters ----------
st.sidebar.header("Filters")
topic_filter = st.sidebar.multiselect(
    "Filter by topic",
    options=sorted(df["topic"].unique()),
    default=sorted(df["topic"].unique()),
)
filtered = df[df["topic"].isin(topic_filter)]
st.sidebar.write(f"Showing {len(filtered)} of {len(df)} assignments")

# ---------- Downloads ----------
st.sidebar.divider()
st.sidebar.download_button(
    "Download analyzed CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="assignments_analyzed.csv",
    mime="text/csv",
)
if (OUT / "summary_report.txt").exists():
    st.sidebar.download_button(
        "Download summary report",
        data=(OUT / "summary_report.txt").read_bytes(),
        file_name="summary_report.txt",
        mime="text/plain",
    )
