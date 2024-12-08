import sqlite3
def fetch_course_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            courses.course_code,
            courses.days,
            courses.start_time,
            courses.end_time,
            courses.open_seats,
            courses.location,
            instructors.name AS instructor_name,
            instructors.biography,
            reviews.quality,
            reviews.difficulty,
            reviews.review_text
        FROM courses
        LEFT JOIN instructors ON courses.instructor_id = instructors.instructor_id
        LEFT JOIN reviews ON instructors.instructor_id = reviews.instructor_id
    """)
    results = cursor.fetchall()

    conn.close()
    return results

# Fetch and display data
course_data = fetch_course_data("class_search_bot.db")
# for row in course_data:
#     print(row)
