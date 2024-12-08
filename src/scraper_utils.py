import os
import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def ensure_directory(path):
    """Ensure the directory exists."""
    os.makedirs(path, exist_ok=True)


def insert_course_data(db_path, data):
    """Insert or update course data into the database."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for course in data:
        try:
            # Ensure instructor exists or insert it
            cursor.execute("""
                INSERT OR IGNORE INTO instructors (name)
                VALUES (?)""",
                (course['Instructor'],)
            )

            # Insert or update course details
            cursor.execute("""
                INSERT OR REPLACE INTO courses 
                (course_code, instructor_id, days, start_time, end_time, open_seats, location)
                SELECT ?, instructor_id, ?, ?, ?, ?, ?
                FROM instructors WHERE name = ?""",
                (course['Course'], course['Days'], course['Start'], 
                 course['End'], course['Open_seats'], course['Location'], course['Instructor'])
            )
        except Exception as e:
            print(f"Failed to insert or update course: {course['Course']} - {e}")


    connection.commit()
    connection.close()

def scrape_courses(driver_path, subject, catalog_number, db_path):
    """Scrape course details for the given subject and catalog number."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://catalog.apps.asu.edu/catalog/classes"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for the term dropdown to be visible
        term_dropdown = wait.until(EC.presence_of_element_located((By.ID, "term")))

        # Retry logic to ensure "Spring 2025" is available
        retries = 5
        for attempt in range(retries):
            available_terms = [option.text for option in Select(term_dropdown).options]
            # print(f"Attempt {attempt + 1}: Available terms - {available_terms}")
            if "Spring 2025" in available_terms:
                Select(term_dropdown).select_by_visible_text("Spring 2025")
                # print("Spring 2025 term selected.")
                break
            else:
                time.sleep(2)  # Wait before retrying
        else:
            raise Exception("Spring 2025 term not found in the dropdown options.")

        # Wait for the page to stabilize after term selection
        time.sleep(3)

        # Input subject
        subject_input = wait.until(EC.presence_of_element_located((By.NAME, "subject")))
        subject_input.clear()
        subject_input.send_keys(subject)

        # Input catalog number
        catalog_number_input = wait.until(EC.presence_of_element_located((By.ID, "catalogNbr")))
        catalog_number_input.clear()
        catalog_number_input.send_keys(catalog_number)

        # Click the "Search Classes" button
        search_button = wait.until(EC.element_to_be_clickable((By.ID, "search-button")))
        search_button.click()

        # Wait for the results table to load
        rows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "class-accordion")))

        # Scrape course information
        data = []
        for row in rows:
            data.append({
                "Course": row.find_element(By.CLASS_NAME, "bold-hyperlink").text.strip(),
                "Instructor": row.find_element(By.CLASS_NAME, "instructor").text.strip(),
                "Days": row.find_element(By.CLASS_NAME, "days").text.strip(),
                "Start": row.find_element(By.CLASS_NAME, "start").text.strip(),
                "End": row.find_element(By.CLASS_NAME, "end").text.strip(),
                "Open_seats": row.find_element(By.CLASS_NAME, "seats").text.strip(),
                "Location": row.find_element(By.CLASS_NAME, "location").text.strip(),
            })

        # Insert data into the database
        insert_course_data(db_path, data)

    finally:
        driver.quit()