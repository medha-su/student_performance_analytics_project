# Student Performance Analytics System

**Python with AI mini project** using Python, NumPy, and Pandas.

## Objective

Read a student dataset and produce understandable analysis of subject marks, totals, averages, grades, pass/fail results, attendance, and top performers.

## Features

- Loads `students.csv` into a Pandas DataFrame.
- Validates required columns, unique IDs, numeric values, and mark/attendance ranges.
- Calculates total and average marks using NumPy.
- Assigns grades using a documented rule and calculates pass/fail status.
- Shows class-level and subject-level statistics.
- Identifies top performers.
- Filters by result, attendance, or department; searches by ID or name.
- Demonstrates `head()`, `tail()`, `info()`, `describe()`, column selection, `iloc`, and boolean filtering.
- Includes reusable functions, loops, conditions, exception handling, classes, encapsulation, inheritance, and method overriding.
- Includes a separate course-concepts demonstration for lists, tuples, sets, dictionaries, Python arrays, random selection, NumPy sequences, normalization, dot product, and ReLU.

## Technologies

- Python 3.9 or later
- NumPy
- Pandas

## Setup

1. Install Python 3.9 or later.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python main.py
   ```

On some Windows systems, use `py main.py` instead of `python main.py`.

## Dataset

The included CSV has 20 **synthetic sample records** and four subject columns: Python, NumPy, Pandas, and AI_Basics. It is sample data for demonstrating the program, not real institutional student data. Replace or adapt it if your instructor requires your own dataset.

## Grading rules used in this project

- Each subject mark must be between 0 and 100.
- Pass: at least 40 marks in **every** subject. Otherwise, Fail.
- Grades based on the average of the four subjects:
  - A+: 90–100
  - A: 80–89.99
  - B: 70–79.99
  - C: 60–69.99
  - D: 50–59.99
  - E: 40–49.99
  - F: below 40
- Attendance status: `Eligible (>=75%)` if attendance is at least 75%; otherwise `Below 75%`.
- These are project rules for demonstration, not official college rules.

## Files

- `main.py` — menu and program entry point
- `functions.py` — reusable functions and analytics classes
- `students.csv` — 20 sample student records
- `Project_Documentation.docx` — project report template/content



## Future Improvements

* Add visual charts for student performance.
* Develop an interactive dashboard.
* Include additional statistical analysis.
* Support larger datasets and additional reporting features.
