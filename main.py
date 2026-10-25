"""
Student Performance Analytics System
"""

from pathlib import Path
import pandas as pd
import numpy as np

from functions import (
    REQUIRED_COLUMNS,
    load_dataset,
    validate_dataset,
    add_performance_columns,
    print_dataset_overview,
    print_overall_analysis,
    print_subject_analysis,
    print_top_performers,
    filter_students,
    search_student,
    show_course_concepts_demo,
    StudentAnalytics,
    DepartmentAnalytics,
)


DATA_FILE = Path(__file__).resolve().parent / "students.csv"


def display_menu():
    """Display the interactive menu using a loop-friendly structure."""
    print("\n" + "=" * 68)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 68)
    print("1. View dataset and dataset information")
    print("2. View overall class and subject analysis")
    print("3. View top-performing students")
    print("4. Filter students by pass/fail or attendance")
    print("5. Search for a student by ID or name")
    print("6. View course-concepts demonstration")
    print("7. Exit")


def run_full_report(df):
    """Run the complete report using reusable functions and class methods."""
    print_dataset_overview(df)
    print_overall_analysis(df)
    print_subject_analysis(df)
    print_top_performers(df)

    # OOP demonstration: base class and child class reuse the analysis data.
    analyzer = StudentAnalytics(df)
    print("\n" + analyzer.report_title())
    print(analyzer.summary_line())

    department_analyzer = DepartmentAnalytics(df, department="Electronics")
    print("\n" + department_analyzer.report_title())
    print(department_analyzer.summary_line())


def main():
    """Program entry point. Exceptions are handled to avoid unexplained crashes."""
    try:
        raw_df = load_dataset(DATA_FILE)
        validate_dataset(raw_df, REQUIRED_COLUMNS)
        df = add_performance_columns(raw_df)
    except FileNotFoundError:
        print(f"ERROR: Dataset not found: {DATA_FILE}")
        print("Keep students.csv in the same folder as main.py.")
        return
    except (ValueError, pd.errors.ParserError) as error:
        print(f"ERROR: Could not load a valid dataset: {error}")
        return
    except Exception as error:
        print(f"Unexpected setup error: {error}")
        return

    print("\nDataset loaded successfully.")
    print(f"Records: {len(df)} | Columns: {len(df.columns)}")
    print("Note: This is an educational analytics tool, not an official grading system.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            print_dataset_overview(df)
        elif choice == "2":

            print_overall_analysis(df)
            print_subject_analysis(df)
        elif choice == "3":
            print_top_performers(df)
        elif choice == "4":
            filter_students(df)
        elif choice == "5":
            search_student(df)
        elif choice == "6":
            show_course_concepts_demo(df)
        elif choice == "7":
            print("Thank you for using Student Performance Analytics System.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
