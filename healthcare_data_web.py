# ============================================================
#  Healthcare AI Informatics Specialist - Week 3 Mini Project
#  Healthcare CSV Data Analyzer - WEB APP VERSION (single file)
#  Concepts: Pandas DataFrames, Data Cleaning, CSV Handling,
#            Matplotlib Visualization (charts shown in browser)
#
#  Install once: pip install flask pandas matplotlib
#  Run:          python healthcare_data_web.py
#  Open browser: http://127.0.0.1:5000
#  Keep "healthcare_sample_data.csv" in the same folder to use
#  the built-in sample, or upload your own CSV from the page.
# ============================================================

import os
import io
import base64
from flask import Flask, request, render_template_string, send_file, redirect, url_for
import pandas as pd
import matplotlib
matplotlib.use("Agg")           # no GUI backend needed for a web server
import matplotlib.pyplot as plt

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.join(BASE_DIR, "healthcare_sample_data.csv")
UPLOAD_FILE = os.path.join(BASE_DIR, "_uploaded_data.csv")
CLEANED_FILE = os.path.join(BASE_DIR, "_cleaned_data.csv")


# --------------------------------------------------------------
# DATA CLEANING FUNCTION (same core Pandas logic as the GUI app)
# --------------------------------------------------------------
def clean_dataset(df):
    report = []
    df = df.copy()

    text_cols = df.select_dtypes(include="object").columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    gender_map = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}
    before_unique = df["Gender"].nunique()
    df["Gender"] = df["Gender"].str.lower().map(gender_map).fillna(df["Gender"])
    report.append(f"Standardized Gender labels ({before_unique} variants -> {df['Gender'].nunique()})")

    df["Diagnosis"] = df["Diagnosis"].str.title()
    report.append("Standardized Diagnosis text to consistent Title Case")

    smoker_map = {"y": "Yes", "yes": "Yes", "n": "No", "no": "No"}
    df["Smoker"] = df["Smoker"].str.lower().map(smoker_map).fillna(df["Smoker"])

    invalid_ages = (df["Age"] < 0).sum()
    df.loc[df["Age"] < 0, "Age"] = pd.NA
    if invalid_ages:
        report.append(f"Fixed {invalid_ages} negative Age values (converted to missing)")

    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    missing_age = df["Age"].isna().sum()
    df["Age"] = df["Age"].fillna(df["Age"].median()).round().astype(int)
    if missing_age:
        report.append(f"Filled {missing_age} missing Age values with the median age")

    for col in ["BloodPressure", "Cholesterol", "BMI"]:
        missing = df[col].isna().sum()
        df[col] = df[col].fillna(round(df[col].mean(), 1))
        if missing:
            report.append(f"Filled {missing} missing {col} values with the column average")

    df["Visit_Date"] = pd.to_datetime(df["Visit_Date"], errors="coerce")

    dupes = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    if dupes:
        report.append(f"Removed {dupes} duplicate patient records")

    return df, report


def fig_to_base64(fig):
    """Convert a matplotlib figure to a base64 string so it can be shown in HTML."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def make_charts(df):
    """Build the 3 analysis charts and return them as base64 images."""
    fig1, ax1 = plt.subplots(figsize=(5, 3.5))
    ax1.hist(df["Age"], bins=10, color="#0f766e", edgecolor="white")
    ax1.set_title("Age Distribution")
    ax1.set_xlabel("Age")
    age_chart = fig_to_base64(fig1)

    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    counts = df["Diagnosis"].value_counts()
    ax2.bar(counts.index, counts.values, color="#0369a1")
    ax2.set_title("Diagnosis Frequency")
    ax2.tick_params(axis="x", rotation=45)
    diag_chart = fig_to_base64(fig2)

    fig3, ax3 = plt.subplots(figsize=(5, 3.5))
    gcounts = df["Gender"].value_counts()
    ax3.pie(gcounts.values, labels=gcounts.index, autopct="%1.0f%%", colors=["#0f766e", "#0369a1"])
    ax3.set_title("Gender Distribution")
    gender_chart = fig_to_base64(fig3)

    return age_chart, diag_chart, gender_chart


# --------------------------------------------------------------
# PAGE STYLE
# --------------------------------------------------------------
STYLE = """
<style>
  body { font-family:'Segoe UI',sans-serif; background:#eaf6f6; margin:0; color:#1e293b; }
  header { background:#0f766e; color:white; padding:18px 30px; }
  header h1 { margin:0; font-size:22px; }
  .container { max-width:1000px; margin:25px auto; padding:0 15px; }
  .card { background:white; border-radius:10px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.08); margin-bottom:20px; }
  table { width:100%; border-collapse:collapse; font-size:13px; }
  th, td { padding:7px; border-bottom:1px solid #e2e8f0; text-align:center; }
  th { background:#f0fdfa; color:#0f766e; }
  .btn { background:#0369a1; color:white; border:none; padding:9px 16px; border-radius:6px;
         text-decoration:none; font-size:13px; cursor:pointer; display:inline-block; margin-right:8px; }
  .btn.primary { background:#0f766e; }
  .btn.grey { background:#64748b; }
  ul.report li { margin:4px 0; }
  .charts { display:flex; gap:15px; flex-wrap:wrap; justify-content:center; }
  .charts img { max-width:31%; border-radius:8px; }
  .stat { display:inline-block; background:#f0fdfa; padding:10px 15px; border-radius:8px; margin:5px; font-size:14px; }
</style>
"""

HOME_PAGE = STYLE + """
<header><h1>📊 Healthcare CSV Data Analyzer</h1></header>
<div class="container">
  <div class="card">
    <h3>Step 1: Choose a Dataset</h3>
    <form method="post" action="/use_sample" style="display:inline;">
      <button class="btn primary" type="submit">Use Built-in Sample Dataset</button>
    </form>
    <form method="post" action="/upload" enctype="multipart/form-data" style="display:inline;">
      <input type="file" name="file" accept=".csv" required>
      <button class="btn" type="submit">Upload My Own CSV</button>
    </form>
  </div>

  {% if raw_preview is not none %}
  <div class="card">
    <h3>Raw Data Preview ({{ raw_shape }} rows x cols)</h3>
    {{ raw_preview | safe }}
    <form method="post" action="/clean" style="margin-top:15px;">
      <button class="btn primary" type="submit">🧹 Clean This Data</button>
    </form>
  </div>
  {% endif %}
</div>
"""

RESULT_PAGE = STYLE + """
<header><h1>📊 Healthcare CSV Data Analyzer - Results</h1></header>
<div class="container">
  <div class="card">
    <h3>Cleaning Report</h3>
    <ul class="report">{% for r in report %}<li>{{ r }}</li>{% endfor %}</ul>
    <a class="btn primary" href="/download">⬇ Download Cleaned CSV</a>
    <a class="btn grey" href="/">⬅ Start Over</a>
  </div>

  <div class="card">
    <h3>Summary Statistics</h3>
    <span class="stat">Total Patients: {{ stats.total }}</span>
    <span class="stat">Avg Age: {{ stats.avg_age }}</span>
    <span class="stat">Avg BMI: {{ stats.avg_bmi }}</span>
    <span class="stat">Avg Cholesterol: {{ stats.avg_chol }}</span>
    <span class="stat">Top Diagnosis: {{ stats.top_diag }}</span>
    <span class="stat">Smokers: {{ stats.smoker_pct }}%</span>
  </div>

  <div class="card">
    <h3>Charts</h3>
    <div class="charts">
      <img src="data:image/png;base64,{{ age_chart }}">
      <img src="data:image/png;base64,{{ diag_chart }}">
      <img src="data:image/png;base64,{{ gender_chart }}">
    </div>
  </div>

  <div class="card">
    <h3>Cleaned Data Preview</h3>
    {{ clean_preview | safe }}
  </div>
</div>
"""


# --------------------------------------------------------------
# ROUTES
# --------------------------------------------------------------
@app.route("/")
def home():
    raw_preview = None
    raw_shape = ""
    if os.path.exists(UPLOAD_FILE):
        df = pd.read_csv(UPLOAD_FILE)
        raw_preview = df.head(8).to_html(index=False)
        raw_shape = f"{df.shape[0]} x {df.shape[1]}"
    return render_template_string(HOME_PAGE, raw_preview=raw_preview, raw_shape=raw_shape)


@app.route("/use_sample", methods=["POST"])
def use_sample():
    if not os.path.exists(SAMPLE_FILE):
        return "<h3>Sample file not found. Please upload your own CSV instead.</h3><a href='/'>Back</a>"
    df = pd.read_csv(SAMPLE_FILE)
    df.to_csv(UPLOAD_FILE, index=False)
    return redirect(url_for("home"))


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("home"))
    try:
        df = pd.read_csv(file)
        df.to_csv(UPLOAD_FILE, index=False)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return "<h3>Could not read that CSV file. Please try another.</h3><a href='/'>Back</a>"
    return redirect(url_for("home"))


@app.route("/clean", methods=["POST"])
def clean():
    if not os.path.exists(UPLOAD_FILE):
        return redirect(url_for("home"))

    raw_df = pd.read_csv(UPLOAD_FILE)
    clean_df, report = clean_dataset(raw_df)
    clean_df.to_csv(CLEANED_FILE, index=False)

    stats = {
        "total": len(clean_df),
        "avg_age": round(clean_df["Age"].mean(), 1),
        "avg_bmi": round(clean_df["BMI"].mean(), 1),
        "avg_chol": round(clean_df["Cholesterol"].mean(), 1),
        "top_diag": clean_df["Diagnosis"].value_counts().idxmax(),
        "smoker_pct": round((clean_df["Smoker"] == "Yes").mean() * 100, 1),
    }
    age_chart, diag_chart, gender_chart = make_charts(clean_df)

    return render_template_string(
        RESULT_PAGE, report=report, stats=stats,
        age_chart=age_chart, diag_chart=diag_chart, gender_chart=gender_chart,
        clean_preview=clean_df.head(10).to_html(index=False)
    )


@app.route("/download")
def download():
    if not os.path.exists(CLEANED_FILE):
        return redirect(url_for("home"))
    return send_file(CLEANED_FILE, as_attachment=True, download_name="cleaned_healthcare_data.csv")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
