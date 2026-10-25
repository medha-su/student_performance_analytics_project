"""Reusable functions and classes for the Student Performance Analytics System."""

from pathlib import Path
import random
from array import array

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "Student_ID", "Name", "Department",
    "Python", "NumPy", "Pandas", "AI_Basics",
    "Attendance_Percent"
]
SUBJECT_COLUMNS = ["Python", "NumPy", "Pandas", "AI_Basics"]
PASS_MARK = 40
ATTENDANCE_THRESHOLD = 75


def load_dataset(file_path):
    """Load a CSV file into a Pandas DataFrame."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find {file_path.name}.")
    return pd.read_csv(file_path)


def validate_dataset(df, required_columns):
    """Check required columns, missing values, duplicates, and numeric ranges."""
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError("Missing required columns: " + ", ".join(missing_columns))

    if df.empty:
        raise ValueError("The dataset contains no student records.")

    if df["Student_ID"].isna().any():
        raise ValueError("Student_ID cannot be empty.")
    if df["Student_ID"].duplicated().any():
        raise ValueError("Student_ID values must be unique.")

    if df[["Name", "Department"]].isna().any().any():
        raise ValueError("Name and Department cannot be empty.")

    numeric_columns = SUBJECT_COLUMNS + ["Attendance_Percent"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        if df[column].isna().any():
            raise ValueError(f"{column} contains a blank or non-numeric value.")
        if not df[column].between(0, 100).all():
            raise ValueError(f"{column} values must be between 0 and 100.")

    return True


def grade_from_average(average):
    """Return a grade using the project's documented thresholds."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    elif average >= PASS_MARK:
        return "E"
    return "F"


def add_performance_columns(df):
    """Return a copy of the dataset with totals, averages, grade, and result."""
    result = df.copy()

    # NumPy arrays are used for numerical calculations and normalization.
    marks_matrix = result[SUBJECT_COLUMNS].to_numpy(dtype=float)
    result["Total_Marks"] = np.sum(marks_matrix, axis=1)
    result["Average_Marks"] = np.mean(marks_matrix, axis=1).round(2)

    # A student must score at least 40 in every subject to pass.
    result["Result"] = np.where((result[SUBJECT_COLUMNS] >= PASS_MARK).all(axis=1),
                                "Pass", "Fail")
    result["Grade"] = result["Average_Marks"].apply(grade_from_average)
    result["Attendance_Status"] = np.where(
        result["Attendance_Percent"] >= ATTENDANCE_THRESHOLD,
        "Eligible (>=75%)",
        "Below 75%"
    )
    result["Normalized_Average"] = (result["Average_Marks"] / 100.0).round(3)
    return result




def print_dataset_overview(df):
    """Display a simple dataset preview and basic information."""

    print("\n" + "=" * 45)
    print("          DATASET OVERVIEW")
    print("=" * 45)

    print(f"Total students: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print("\n--- FIRST 5 STUDENTS ---")
    columns_to_show = [
        "Student_ID",
        "Name",
        "Average_Marks",
        "Grade",
        "Result"
    ]
    print(df[columns_to_show].head().to_string(index=False))

    print("\n--- FIRST STUDENT ---")
    first_student = df.iloc[0]
    print(f"Name: {first_student['Name']}")
    print(f"Average: {first_student['Average_Marks']:.2f}")
    print(f"Grade: {first_student['Grade']}")
    print(f"Result: {first_student['Result']}")

    print("\n--- NUMERIC SUMMARY ---")
    print(f"Class average: {df['Average_Marks'].mean():.2f}")
    print(f"Highest average: {df['Average_Marks'].max():.2f}")
    print(f"Lowest average: {df['Average_Marks'].min():.2f}")

    # Demonstrate Pandas methods without printing large tables.
    df.info(verbose=False)
    summary = df.describe()



def print_overall_analysis(df):
    """Print class-level statistics, pass/fail counts, and attendance information."""
    print("\n--- OVERALL PERFORMANCE ANALYSIS ---")
    averages = df["Average_Marks"].to_numpy(dtype=float)

    print(f"Number of students       : {df['Student_ID'].count()}")
    print(f"Class average            : {np.mean(averages):.2f}")
    print(f"Highest student average  : {np.max(averages):.2f}")
    print(f"Lowest student average   : {np.min(averages):.2f}")
    print(f"Total marks scored       : {int(df['Total_Marks'].sum())}")
    print(f"Students passed          : {(df['Result'] == 'Pass').sum()}")
    print(f"Students failed          : {(df['Result'] == 'Fail').sum()}")
    print(f"Average attendance       : {df['Attendance_Percent'].mean():.2f}%")
    print(f"Below 75% attendance     : {(df['Attendance_Percent'] < ATTENDANCE_THRESHOLD).sum()}")

    print("\n--- RESULT FILTER: PASS STUDENTS ---")
    passed_df = df[df["Result"] == "Pass"]
    print(passed_df[["Student_ID", "Name", "Average_Marks", "Grade"]].to_string(index=False)
          if not passed_df.empty else "No students meet the pass rule.")


def print_subject_analysis(df):
    """Calculate and rank the average, highest, and lowest marks per subject."""
    print("\n--- SUBJECT-WISE PERFORMANCE ---")
    subject_means = df[SUBJECT_COLUMNS].mean().sort_values(ascending=False)
    for subject, average in subject_means.items():
        print(f"{subject:12s} average: {average:.2f}")

    print(f"\nBest-performing subject : {subject_means.index[0]} ({subject_means.iloc[0]:.2f})")
    print(f"Lowest-performing subject: {subject_means.index[-1]} ({subject_means.iloc[-1]:.2f})")
    print("\nSubject maximum marks:")
    print(df[SUBJECT_COLUMNS].max().to_string())
    print("\nSubject minimum marks:")
    print(df[SUBJECT_COLUMNS].min().to_string())


def print_top_performers(df, top_n=5):
    """Display top performers, preserving ties at the cutoff average."""
    print(f"\n--- TOP {top_n} STUDENTS ---")
    top_df = df.nlargest(top_n, "Average_Marks")
    print(top_df[["Student_ID", "Name", "Department", "Average_Marks",
                  "Grade", "Result"]].to_string(index=False))


def filter_students(df):
    """Filter using user input and boolean conditions."""
    print("\nFilter options: 1 = Pass, 2 = Fail, 3 = Attendance below 75%, 4 = Department")
    choice = input("Choose filter (1-4): ").strip()

    if choice == "1":
        filtered = df[df["Result"] == "Pass"]
    elif choice == "2":
        filtered = df[df["Result"] == "Fail"]
    elif choice == "3":
        filtered = df[df["Attendance_Percent"] < ATTENDANCE_THRESHOLD]
    elif choice == "4":
        departments = sorted(df["Department"].dropna().astype(str).unique())
        print("Available departments:", ", ".join(departments))
        department = input("Enter department name: ").strip()
        filtered = df[df["Department"].str.casefold() == department.casefold()]
    else:
        print("Invalid filter option.")
        return

    if filtered.empty:
        print("No matching student records found.")
    else:
        print(filtered[["Student_ID", "Name", "Department", "Average_Marks",
                        "Grade", "Result", "Attendance_Percent"]].to_string(index=False))


def search_student(df):
    """Search by student ID or partial name, ignoring name capitalization."""
    query = input("Enter Student ID or part of the student's name: ").strip()
    if not query:
        print("Search cannot be empty.")
        return

    matches = df[
        df["Student_ID"].astype(str).str.casefold().eq(query.casefold())
        | df["Name"].astype(str).str.contains(query, case=False, na=False)
    ]
    if matches.empty:
        print("No matching student found.")
    else:
        print(matches.to_string(index=False))


class StudentAnalytics:
    """Base analytics class; demonstrates encapsulation with a private DataFrame."""

    def __init__(self, dataframe):
        self.__dataframe = dataframe.copy()

    def get_dataframe(self):
        """Getter method returns a copy rather than exposing internal data."""
        return self.__dataframe.copy()

    def report_title(self):
        """A child class may override this method (polymorphism)."""
        return "Student Analytics Summary"

    def summary_line(self):
        dataframe = self.get_dataframe()
        return (
            f"{len(dataframe)} students | class average "
            f"{dataframe['Average_Marks'].mean():.2f} | "
            f"{(dataframe['Result'] == 'Pass').sum()} passed"
        )


class DepartmentAnalytics(StudentAnalytics):
    """Child class that overrides report_title and filters a department."""

    def __init__(self, dataframe, department):
        super().__init__(dataframe)
        self.department = department

    def report_title(self):
        return f"Department Analytics: {self.department}"

    def summary_line(self):
        dataframe = self.get_dataframe()
        department_df = dataframe[
            dataframe["Department"].str.casefold() == self.department.casefold()
        ]
        if department_df.empty:
            return f"No records found for department '{self.department}'."
        return (
            f"{len(department_df)} students | average "
            f"{department_df['Average_Marks'].mean():.2f} | "
            f"{(department_df['Result'] == 'Pass').sum()} passed"
        )


def show_course_concepts_demo(df):
    """Demonstrate selected taught concepts in a relevant, non-grading side panel."""
    print("\n--- PYTHON WITH AI COURSE CONCEPTS DEMO ---")

    # Lists, tuples, sets, and dictionaries (Day 5 concepts).
    subjects_list = list(SUBJECT_COLUMNS)
    subject_tuple = tuple(SUBJECT_COLUMNS)
    departments_set = set(df["Department"].astype(str))
    project_details = {
        "project": "Student Performance Analytics System",
        "records": len(df),
        "subjects": len(subjects_list),
    }
    print("Subjects list :", subjects_list)
    print("Subjects tuple:", subject_tuple)
    print("Departments set (unique values):", sorted(departments_set))
    print("Project dictionary:", project_details)

    # array module (Day 7): homogeneous numeric data and array manipulation.
    sample_marks = array("f", df[SUBJECT_COLUMNS[0]].head(4).astype(float).tolist())
    print("Python float array (first four Python marks):", list(sample_marks))
    if len(sample_marks) > 0:
        sample_marks.append(0.0)
        print("Array after append(0.0):", list(sample_marks))

    # random module (Day 7): select one sample record for demonstration only.
    sample_name = random.choice(df["Name"].astype(str).tolist())
    print("Randomly selected sample student (not a ranking):", sample_name)

    # NumPy sequence, zeros/ones, normalization, dot product and ReLU (Day 9).
    sequence = np.arange(1, 6)
    zeros = np.zeros(3)
    ones = np.ones((2, 2))
    normalized = df[SUBJECT_COLUMNS].iloc[0].to_numpy(dtype=float) / 100.0
    weights = np.array([0.25, 0.25, 0.25, 0.25])
    neuron_value = float(np.dot(normalized, weights))
    relu_value = float(np.maximum(0, neuron_value))
    print("NumPy sequence np.arange(1, 6):", sequence)
    print("NumPy zeros:", zeros)
    print("NumPy ones matrix:\n", ones)
    print("First student's normalized subject marks:", normalized.round(2))
    print(f"Illustrative dot product + ReLU score: {relu_value:.3f}")
    print("Note: This illustrative value is a course-concept demonstration, not an AI prediction.")
