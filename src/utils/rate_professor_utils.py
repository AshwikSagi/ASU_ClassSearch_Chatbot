import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import random
import time


def initialize_webdriver(driver_path):
    """Initialize the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)


def insert_review_data(db_path, data):
    """Insert or update professor review data into the database."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for review in data:
        try:
            cursor.execute("""
    INSERT OR REPLACE INTO reviews 
    (instructor_id, course, quality, difficulty, attendance, would_take_again, grade, review_text)
    SELECT instructor_id, ?, ?, ?, ?, ?, ?, ?
    FROM instructors WHERE name = ?""",
    (review['Course'], review['Quality'], review['Difficulty'], 
     review['Attendance'], review['Would Take Again'], review['Grade'], 
     review['Review'], review['Instructor']))
        except Exception as e:
            print(f"Failed to insert or update review for instructor {review['Instructor']} - {e}")

    connection.commit()
    connection.close()


def scrape_professor_reviews(driver_path, db_path):
    """Scrape reviews for professors listed in the database."""
    driver = initialize_webdriver(driver_path)

    # Fetch instructor names from the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM instructors")
    instructors = [row[0] for row in cursor.fetchall()]
    connection.close()

    all_reviews_data = []

    try:
        for instructor_name in instructors:
            print(f"Scraping reviews for: {instructor_name}")

            # Search for professor on Google
            search_query = f"{instructor_name} Arizona State University Rate My Professors"
            driver.get("https://www.google.com")
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys(search_query)
            search_box.submit()

            # Click on the first result
            try:
                first_result = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
                )
                first_result.click()
            except Exception as e:
                print(f"Failed to click on the first result for {instructor_name}: {e}")
                continue

            # Extract reviews
            try:
                review_cards = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "Rating__RatingBody-sc-1rhvpxz-0"))
                )
                for card in review_cards:
                    try:
                        # Extract Course using BeautifulSoup for cleaner parsing
                        course_html = card.find_element(By.XPATH, ".//div[contains(@class, 'RatingHeader__StyledClass-sc-1dlkqw1-3')]").get_attribute('innerHTML')
                        soup = BeautifulSoup(course_html, 'html.parser')
                        course = soup.get_text().strip()
                        if not course or "img" in course_html.lower():
                            course = "N/A"
                    except Exception as e:
                        print(f"Error extracting course for {instructor_name}: {e}")
                        course = "N/A"

                    try:
                        # Extract Quality
                        quality = card.find_element(By.XPATH, ".//div[contains(@class, 'CardNumRating__CardNumRatingNumber') and preceding-sibling::div[text()='Quality']]").text
                    except Exception:
                        quality = "N/A"

                    try:
                        # Extract Difficulty
                        difficulty = card.find_element(By.XPATH, ".//div[contains(@class, 'CardNumRating__CardNumRatingNumber') and preceding-sibling::div[text()='Difficulty']]").text
                    except Exception:
                        difficulty = "N/A"

                    try:
                        # Extract Attendance
                        attendance = card.find_element(By.XPATH, ".//div[contains(text(), 'Attendance')]/span").text
                    except Exception:
                        attendance = "N/A"

                    try:
                        # Extract Would Take Again
                        would_take_again = card.find_element(By.XPATH, ".//div[contains(text(), 'Would Take Again')]/span").text
                    except Exception:
                        would_take_again = "N/A"

                    try:
                        # Extract Grade
                        grade = card.find_element(By.XPATH, ".//div[contains(text(), 'Grade')]/span").text
                    except Exception:
                        grade = "N/A"

                    try:
                        # Extract Review
                        review = card.find_element(By.CLASS_NAME, "Comments__StyledComments-dzzyvm-0").text
                    except Exception:
                        review = "N/A"

                    # Append to list
                    all_reviews_data.append({
                        "Instructor": instructor_name,
                        "Course": course,
                        "Quality": quality,
                        "Difficulty": difficulty,
                        "Attendance": attendance,
                        "Would Take Again": would_take_again,
                        "Grade": grade,
                        "Review": review,
                    })
            except Exception as e:
                print(f"No reviews found for {instructor_name}: {e}")
                continue

            # Introduce a short delay to avoid detection
            time.sleep(random.uniform(2, 5))

        # Insert data into the database
        insert_review_data(db_path, all_reviews_data)

    finally:
        driver.quit()