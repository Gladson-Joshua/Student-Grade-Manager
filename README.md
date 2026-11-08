# 🎓 Student Grade Manager

A simple Streamlit web app for entering student marks, assigning letter grades automatically, and showing basic class statistics.

## Features

- Add students with a name and a mark (0–100)
- Letter grade assigned automatically
- Results shown in a table
- Class average, highest and lowest marks
- Clear all records with one click
- Input validation:
  - Name cannot be empty or only spaces
  - Name must contain at least one letter
  - Name must be 50 characters or fewer
  - Duplicate names are rejected (case-insensitive)
  - Extra spaces in names are trimmed

## Grading Scale

| Mark   | Grade |
|--------|-------|
| 90–100 | A     |
| 80–89  | B     |
| 70–79  | C     |
| 60–69  | D     |
| 0–59   | E     |

## Requirements

- Python 3.9 or later
- Packages listed in `requirements.txt` (Streamlit, pandas)

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run grade_app.py
```

The app opens in your browser at `http://localhost:8501`.

## Usage

1. Enter the student's name and mark.
2. Click **Add Student**.
3. The student appears in the **Student Results** table with their grade.
4. The summary metrics update automatically.
5. Click **Clear All Students** to start over.

> **Note:** Records live only in the current browser session (`st.session_state`). They are lost when the page is refreshed or the app restarts.

## Project Structure

```
.
├── grade_app.py      # Streamlit application
├── requirements.txt  # Python dependencies
└── README.md
```
