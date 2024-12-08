import pandas as pd
import sqlite3
import os


def check_file_validity(filepath):
    """Ensure the file exists and is not empty."""
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        raise FileNotFoundError(f"The file {filepath} is missing or empty.")


def insert_data(db_path, faculty_profiles_csv, rate_my_professors_csv):
    """Insert faculty profiles and reviews into the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert faculty profiles
    profiles = pd.read_csv(faculty_profiles_csv)
    for _, row in profiles.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO instructors (name, biography, google_scholar_url, research_website_url, experts_asu_url)
            VALUES (?, ?, ?, ?, ?)
        """, (row['Instructor'], row['Biography'], row['Google Scholar URL'], row['Research Website URL'], row['Experts.asu.edu URL']))

    # Insert reviews
    reviews = pd.read_csv(rate_my_professors_csv)
    for _, row in reviews.iterrows():
        cursor.execute("""
            INSERT INTO reviews (instructor_id,course, quality, difficulty, attendance, would_take_again, grade, review_text)
            SELECT instructor_id, ?, ?, ?, ?, ?, ?
            FROM instructors WHERE name = ?""",
            (row['Quality'], row['Difficulty'], row['Attendance'], row['Would Take Again'], row['Grade'], row['Review'], row['Instructor'])
        )

    conn.commit()
    conn.close()