import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup

def initialize_webdriver(driver_path):
    """Initialize the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def insert_faculty_data(db_path, data):
    """Insert or update faculty data into the database."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for faculty in data:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO instructors 
                (name, biography, google_scholar_url, research_website_url, experts_asu_url)
                VALUES (?, ?, ?, ?, ?)""",
                (faculty["Instructor"], faculty["Biography"], 
                 faculty["Google Scholar URL"], faculty["Research Website URL"], 
                 faculty["Experts.asu.edu URL"])
            )
        except Exception as e:
            print(f"Failed to insert or update faculty profile for {faculty['Instructor']} - {e}")

    connection.commit()
    connection.close()

def search_faculty(driver, instructor_name):
    """Search for faculty profile on Google."""
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(f"{instructor_name} ASU employee directory")
    search_box.submit()

    try:
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
        )
        first_result.click()
        return True
    except Exception as e:
        print(f"Failed to click on the first result for {instructor_name}: {e}")
        return False

def scrape_faculty_profiles(driver_path, db_path):
    """Scrape faculty profiles."""
    driver = initialize_webdriver(driver_path)

    # Fetch instructor names from the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM instructors WHERE biography IS NULL OR biography = ''")
    instructors = [row[0] for row in cursor.fetchall()]
    connection.close()

    if not instructors:
        print("No instructors to scrape. All profiles may already be complete.")
        return

    all_faculty_data = []
    try:
        for instructor in instructors:
            print(f"Scraping profile for: {instructor}")

            if not search_faculty(driver, instructor):
                continue

            faculty_details = {
                "Instructor": instructor,
                "Biography": "N/A",
                "Google Scholar URL": "N/A",
                "Research Website URL": "N/A",
                "Experts.asu.edu URL": "N/A",
            }

            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract faculty biography
            try:
                bio_div = soup.find("div", {"class": "user__field-profile-biography"})
                faculty_details["Biography"] = bio_div.find("div", {"class": "field__item"}).get_text(strip=True)
            except Exception:
                print(f"Biography not found for {instructor}.")

            # Extract research information
            try:
                research_section = soup.find("div", {"id": "nav-group-research"})

                # Google Scholar URL
                google_scholar_div = research_section.find("div", {"class": "user__field-profile-google-scholar"})
                if google_scholar_div:
                    faculty_details["Google Scholar URL"] = google_scholar_div.find("a").get("href", "N/A")

                # Research Website URL
                research_website_div = research_section.find("div", {"class": "user__field-profile-research-website"})
                if research_website_div:
                    faculty_details["Research Website URL"] = research_website_div.find("a").get("href", "N/A")

                # Experts.asu.edu URL
                experts_div = research_section.find("div", {"class": "user__field-profile-experts-asu"})
                if experts_div:
                    faculty_details["Experts.asu.edu URL"] = experts_div.find("a").get("href", "N/A")
            except Exception as e:
                print(f"Error scraping research information for {instructor}: {e}")

            all_faculty_data.append(faculty_details)
            # print(f"Scraped data for: {instructor}: {faculty_details}")

        # Insert data into the database
        insert_faculty_data(db_path, all_faculty_data)

    finally:
        driver.quit()