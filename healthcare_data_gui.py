# ============================================================
#  Healthcare AI Informatics Specialist - Week 3 Mini Project
#  Healthcare CSV Data Analyzer - GUI VERSION (single file)
#  Concepts: Pandas Series & DataFrames, Data Cleaning,
#            CSV Handling, Matplotlib Visualization
#
#  Run:  python healthcare_data_gui.py
#  Needs: pandas, matplotlib   ->  pip install pandas matplotlib
#  Keep "healthcare_sample_data.csv" in the same folder,
#  or use the "Load CSV" button to pick your own file.
# ============================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

COLOR_PRIMARY = "#0f766e"
COLOR_ACCENT = "#0369a1"
COLOR_BG = "#eaf6f6"
COLOR_CARD = "#ffffff"

raw_df = None       # original loaded data
clean_df = None      # cleaned data
current_file = ""

# --------------------------------------------------------------
# DATA CLEANING FUNCTION (core Pandas logic)
# --------------------------------------------------------------
def clean_dataset(df):
    """Takes a messy healthcare DataFrame and returns a cleaned copy + a report."""
    report = []
    df = df.copy()

    # 1) Strip extra whitespace from text columns
    text_cols = df.select_dtypes(include="object").columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # 2) Standardize Gender values
    gender_map = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}
    before_unique = df["Gender"].nunique()
    df["Gender"] = df["Gender"].str.lower().map(gender_map).fillna(df["Gender"])
    report.append(f"Standardized Gender labels ({before_unique} variants -> {df['Gender'].nunique()})")

    # 3) Standardize Diagnosis text case
    df["Diagnosis"] = df["Diagnosis"].str.title()
    report.append("Standardized Diagnosis text to consistent Title Case")

    # 4) Standardize Smoker column to Yes/No
    smoker_map = {"y": "Yes", "yes": "Yes", "n": "No", "no": "No"}
    df["Smoker"] = df["Smoker"].str.lower().map(smoker_map).fillna(df["Smoker"])

    # 5) Fix invalid (negative) ages -> treat as missing
    invalid_ages = (df["Age"] < 0).sum()
    df.loc[df["Age"] < 0, "Age"] = pd.NA
    if invalid_ages:
        report.append(f"Fixed {invalid_ages} negative Age values (converted to missing)")

    # 6) Fill missing numeric values with column median/mean
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

    # 7) Convert Visit_Date to a real datetime type
    df["Visit_Date"] = pd.to_datetime(df["Visit_Date"], errors="coerce")

    # 8) Remove duplicate rows
    dupes = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    if dupes:
        report.append(f"Removed {dupes} duplicate patient records")

    return df, report


# --------------------------------------------------------------
# GUI SETUP
# --------------------------------------------------------------
root = tk.Tk()
root.title("Healthcare AI Informatics Specialist - CSV Data Analyzer")
root.geometry("950x650")
root.configure(bg=COLOR_BG)

header = tk.Frame(root, bg=COLOR_PRIMARY)
header.pack(fill="x")
tk.Label(header, text="📊 Healthcare CSV Data Analyzer", font=("Segoe UI", 16, "bold"),
          bg=COLOR_PRIMARY, fg="white").pack(pady=10)

toolbar = tk.Frame(root, bg=COLOR_BG)
toolbar.pack(fill="x", padx=15, pady=10)

file_label = tk.Label(toolbar, text="No file loaded", bg=COLOR_BG, fg="#475569", font=("Segoe UI", 9))
file_label.pack(side="left", padx=5)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=10)

tab_raw = tk.Frame(notebook, bg=COLOR_CARD)
tab_clean = tk.Frame(notebook, bg=COLOR_CARD)
tab_stats = tk.Frame(notebook, bg=COLOR_CARD)
tab_charts = tk.Frame(notebook, bg=COLOR_CARD)
notebook.add(tab_raw, text="1. Raw Data")
notebook.add(tab_clean, text="2. Cleaned Data")
notebook.add(tab_stats, text="3. Analysis")
notebook.add(tab_charts, text="4. Charts")


def make_table(parent, df):
    """Draw a DataFrame inside a Treeview table."""
    for widget in parent.winfo_children():
        widget.destroy()
    if df is None:
        return
    table = ttk.Treeview(parent, columns=list(df.columns), show="headings", height=18)
    for col in df.columns:
        table.heading(col, text=col)
        table.column(col, width=100, anchor="center")
    for _, row in df.iterrows():
        table.insert("", "end", values=list(row))
    table.pack(fill="both", expand=True, padx=10, pady=10)


def load_csv(path=None):
    """Load a CSV file into raw_df and display it."""
    global raw_df, current_file
    try:
        if path is None:
            path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if not path:
                return
        raw_df = pd.read_csv(path)
        current_file = os.path.basename(path)
        file_label.config(text=f"Loaded: {current_file}  ({len(raw_df)} rows)")
        make_table(tab_raw, raw_df)
        notebook.select(tab_raw)
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        messagebox.showerror("Load Error", f"Could not read CSV file:\n{e}")


def run_cleaning():
    """Clean the loaded data and show results + summary."""
    global clean_df
    if raw_df is None:
        messagebox.showwarning("No Data", "Please load a CSV file first.")
        return
    clean_df, report = clean_dataset(raw_df)
    make_table(tab_clean, clean_df)
    notebook.select(tab_clean)
    messagebox.showinfo("Cleaning Complete", "\n".join(report) if report else "Data was already clean!")


def show_analysis():
    """Display summary statistics of the cleaned data."""
    for widget in tab_stats.winfo_children():
        widget.destroy()
    if clean_df is None:
        tk.Label(tab_stats, text="Please clean the data first (Tab 2).", bg=COLOR_CARD,
                 font=("Segoe UI", 11)).pack(pady=30)
        return

    total = len(clean_df)
    avg_age = round(clean_df["Age"].mean(), 1)
    avg_bmi = round(clean_df["BMI"].mean(), 1)
    avg_chol = round(clean_df["Cholesterol"].mean(), 1)
    top_diagnosis = clean_df["Diagnosis"].value_counts().idxmax()
    smoker_pct = round((clean_df["Smoker"] == "Yes").mean() * 100, 1)

    stats_text = (
        f"Total Patients: {total}\n"
        f"Average Age: {avg_age} years\n"
        f"Average BMI: {avg_bmi}\n"
        f"Average Cholesterol: {avg_chol}\n"
        f"Most Common Diagnosis: {top_diagnosis}\n"
        f"Smoker Percentage: {smoker_pct}%\n"
    )
    tk.Label(tab_stats, text="Summary Statistics", font=("Segoe UI", 13, "bold"),
             bg=COLOR_CARD, fg=COLOR_PRIMARY).pack(pady=(20, 5))
    tk.Label(tab_stats, text=stats_text, font=("Segoe UI", 11), bg=COLOR_CARD,
             justify="left").pack(pady=10)

    tk.Label(tab_stats, text="Diagnosis Breakdown", font=("Segoe UI", 12, "bold"),
             bg=COLOR_CARD, fg=COLOR_PRIMARY).pack(pady=(15, 5))
    counts = clean_df["Diagnosis"].value_counts()
    for name, count in counts.items():
        tk.Label(tab_stats, text=f"{name}: {count} patients", bg=COLOR_CARD,
                 font=("Segoe UI", 10)).pack()


def show_charts():
    """Render 3 matplotlib charts inside the Charts tab."""
    for widget in tab_charts.winfo_children():
        widget.destroy()
    if clean_df is None:
        tk.Label(tab_charts, text="Please clean the data first (Tab 2).", bg=COLOR_CARD,
                 font=("Segoe UI", 11)).pack(pady=30)
        return

    fig, axes = plt.subplots(1, 3, figsize=(11, 4))

    axes[0].hist(clean_df["Age"], bins=10, color=COLOR_PRIMARY, edgecolor="white")
    axes[0].set_title("Age Distribution")
    axes[0].set_xlabel("Age")

    diag_counts = clean_df["Diagnosis"].value_counts()
    axes[1].bar(diag_counts.index, diag_counts.values, color=COLOR_ACCENT)
    axes[1].set_title("Diagnosis Frequency")
    axes[1].tick_params(axis="x", rotation=45)

    gender_counts = clean_df["Gender"].value_counts()
    axes[2].pie(gender_counts.values, labels=gender_counts.index, autopct="%1.0f%%",
                colors=["#0f766e", "#0369a1"])
    axes[2].set_title("Gender Distribution")

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=tab_charts)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


def export_cleaned():
    """Save the cleaned DataFrame to a new CSV file."""
    if clean_df is None:
        messagebox.showwarning("No Data", "Please clean the data first.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")],
                                          initialfile="cleaned_healthcare_data.csv")
    if path:
        clean_df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Cleaned data saved to:\n{path}")


# ---------------- Toolbar buttons ----------------
tk.Button(toolbar, text="📂 Load CSV", command=lambda: load_csv(), bg=COLOR_ACCENT, fg="white",
          bd=0, padx=12, pady=5).pack(side="left", padx=5)
tk.Button(toolbar, text="🧹 Clean Data", command=run_cleaning, bg=COLOR_PRIMARY, fg="white",
          bd=0, padx=12, pady=5).pack(side="left", padx=5)
tk.Button(toolbar, text="📈 Analyze", command=show_analysis, bg=COLOR_PRIMARY, fg="white",
          bd=0, padx=12, pady=5).pack(side="left", padx=5)
tk.Button(toolbar, text="📊 Show Charts", command=show_charts, bg=COLOR_PRIMARY, fg="white",
          bd=0, padx=12, pady=5).pack(side="left", padx=5)
tk.Button(toolbar, text="💾 Export Cleaned CSV", command=export_cleaned, bg="#64748b", fg="white",
          bd=0, padx=12, pady=5).pack(side="left", padx=5)

# Auto-load the bundled sample dataset if it exists in the same folder
default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "healthcare_sample_data.csv")
if os.path.exists(default_path):
    load_csv(default_path)

root.mainloop()
