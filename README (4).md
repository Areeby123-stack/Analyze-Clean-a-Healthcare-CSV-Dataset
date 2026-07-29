# 🏥 Healthcare AI Informatics Specialist

<p align="center">
  <img src="assets/banner.svg" alt="Healthcare AI Informatics Specialist Banner" width="100%">
</p>

> A hands-on Python learning journey — building real, working healthcare applications week by week. Every project is **100% offline**, beginner-friendly, and built from scratch using core Python concepts.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-brightgreen)
![Offline](https://img.shields.io/badge/Runs-100%25%20Offline-teal)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📖 About This Project

This repository documents a **week-by-week Python learning roadmap** focused on Healthcare AI & Informatics. Each week introduces new Python concepts and ends with a real mini-project — a working desktop app, web app, or both — themed around healthcare data and patient management.

No external APIs, no internet dependency, no complicated setup. Just clean Python, `tkinter`, `pandas`, and `Flask`.

---

## 🗂️ Repository Structure

```
healthcare-ai-informatics-specialist/
│
├── week1/
│   └── healthcare_ai_quiz.py        # MCQ Quiz App (Tkinter GUI)
│
├── week2/
│   ├── patient_manager.py           # Core OOP module (Patient + PatientManager classes)
│   ├── patient_gui.py               # Patient Management System - Desktop GUI
│   ├── patient_app_single.py        # Same GUI app, bundled into ONE file
│   └── patient_web.py               # Patient Management System - Web App (Flask)
│
├── week3/
│   ├── healthcare_sample_data.csv   # Sample messy healthcare dataset
│   ├── healthcare_data_gui.py       # CSV Data Analyzer - Desktop GUI
│   └── healthcare_data_web.py       # CSV Data Analyzer - Web App (Flask)
│
├── assets/
│   └── banner.svg                   # Project banner image
│
└── README.md
```

---

## 🧭 Weekly Breakdown

### 📌 Week 1 — Python Basics & Setup
**Topics:** Variables, Data Types, Operators, Control Flow, Functions, Error Handling

**Deliverable:** `healthcare_ai_quiz.py`
A stylish, offline MCQ quiz app on **Healthcare AI Informatics** topics (EHR, CDSS, HIPAA, NLP, telemedicine, and more).

| Feature | Description |
|---|---|
| 🎯 Topic-based MCQs | 10 questions on real healthcare informatics concepts |
| 👤 Name capture | Asks the user's name before starting |
| 🔀 Randomized order | Questions shuffle on every attempt |
| 📊 Score + Review | Shows final score, pass/fail, and a full answer review at the end |
| 🎨 Themed UI | Teal & blue healthcare-styled interface (built with `tkinter`) |

```bash
python healthcare_ai_quiz.py
```

---

### 📌 Week 2 — OOP & Data Structures
**Topics:** Classes & Objects, Lists, Dictionaries, Tuples, Sets, List Comprehensions, File Handling

**Deliverable:** Patient Management System — built **twice**: once as a Desktop GUI, once as a Web App, sharing the same data file so both stay in sync.

| Concept | Where It's Used |
|---|---|
| 🧬 Classes & Objects | `Patient` class (medical attributes) + `PatientManager` class (collection logic) |
| 📋 Lists | Patient records, medical history log |
| 🔑 Dictionaries | Fast patient lookup by ID |
| 🔒 Tuples | Vitals snapshot — Blood Pressure & Heart Rate (immutable) |
| 🧩 Sets | Allergies (no duplicates), unique blood group tracking |
| ⚡ List Comprehensions | Search, filter, and delete operations |
| 💾 File Handling | Patient records persist in a shared `patients_data.json` |

**Run the GUI:**
```bash
python patient_gui.py
# or the single-file version (no other files needed):
python patient_app_single.py
```

**Run the Web App:**
```bash
pip install flask
python patient_web.py
# then open: http://127.0.0.1:5000
```

---

### 📌 Week 3 — Pandas & Basic Data Analysis
**Topics:** Pandas Series & DataFrames, Data Cleaning, CSV Handling, Matplotlib Visualization

**Deliverable:** A tool that analyzes and cleans a **realistic, messy healthcare dataset** — again available as both a Desktop GUI and a Web App.

The included `healthcare_sample_data.csv` intentionally contains:
- ❌ Missing values (Age, BMI, Cholesterol, Blood Pressure)
- ❌ Inconsistent labels (`M`, `Male`, `male` → should all mean the same thing)
- ❌ Invalid data (negative ages)
- ❌ Duplicate patient records

| Feature | Description |
|---|---|
| 🧹 One-click Cleaning | Fixes whitespace, standardizes labels, fills missing values, removes duplicates |
| 📈 Auto Analysis | Total patients, average age/BMI/cholesterol, top diagnosis, smoker % |
| 📊 Visual Charts | Age histogram, Diagnosis bar chart, Gender pie chart (via `matplotlib`) |
| 💾 Export | Download the cleaned dataset as a fresh CSV file |

**Run the GUI:**
```bash
pip install pandas matplotlib
python healthcare_data_gui.py
```

**Run the Web App:**
```bash
pip install flask pandas matplotlib
python healthcare_data_web.py
# then open: http://127.0.0.1:5000
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **Tkinter** | Desktop GUI apps (built into Python — no install needed) |
| **Flask** | Lightweight local web apps |
| **Pandas** | Data cleaning & analysis |
| **Matplotlib** | Data visualization / charts |

> ✅ Everything runs **locally and offline** — no internet connection or external API is required once the packages are installed.

---

## ⚙️ Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/healthcare-ai-informatics-specialist.git
cd healthcare-ai-informatics-specialist

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# 3. Install dependencies used across all weeks
pip install flask pandas matplotlib

# 4. Run any project, e.g.:
cd week1
python healthcare_ai_quiz.py
```

---

## 🎯 Learning Outcomes

By completing this roadmap, the following core Python skills were practiced and applied to real healthcare-themed problems:

- ✅ Python fundamentals — variables, control flow, functions, error handling
- ✅ Object-Oriented Programming — designing classes that model real-world entities
- ✅ Core data structures — lists, dicts, tuples, sets, and comprehensions
- ✅ File handling — reading/writing JSON and CSV for persistent data
- ✅ Data analysis — cleaning, transforming, and summarizing real-world messy data with Pandas
- ✅ Data visualization — communicating insights through charts
- ✅ GUI development with Tkinter
- ✅ Web development basics with Flask

---

## 📌 Roadmap

- [x] Week 1 — Python Basics (Quiz App)
- [x] Week 2 — OOP & Data Structures (Patient Management System)
- [x] Week 3 — Pandas & Data Analysis (Healthcare CSV Analyzer)
- [ ] Week 4 — Coming soon...

---

## 📄 License

This project is open-sourced for learning purposes under the [MIT License](LICENSE).

---

<p align="center">Built as part of a self-paced <b>Healthcare AI Informatics Specialist</b> learning path 🩺💻</p>
