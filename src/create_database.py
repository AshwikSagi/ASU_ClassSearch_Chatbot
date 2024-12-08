import sqlite3

def create_database(db_path="../database/class_search_bot.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            biography TEXT,
            google_scholar_url TEXT,
            research_website_url TEXT,
            experts_asu_url TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT,
            instructor_id INTEGER,
            days TEXT,
            start_time TEXT,
            end_time TEXT,
            open_seats TEXT,
            location TEXT,
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            instructor_id INTEGER,
            course TEXT,
            quality FLOAT,
            difficulty FLOAT,
            attendance TEXT,
            would_take_again TEXT,
            grade TEXT,
            review_text TEXT,
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
        )
    """)
    conn.commit()
    conn.close()

# Call the function to create the database
create_database()