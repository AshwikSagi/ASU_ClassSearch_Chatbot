import os
import subprocess
import sys

# Add the parent directory of 'src' to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils.scraper_utils import scrape_courses
from src.utils.rate_professor_utils import scrape_professor_reviews
from src.utils.faculty_profiles_utils import scrape_faculty_profiles
from database.create_database import create_database

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data/raw")
DATABASE_DIR = os.path.join(BASE_DIR, "../database")
DB_PATH = os.path.join(DATABASE_DIR, "class_search_bot.db")
CHROME_DRIVER_PATH = "/Users/ashwiksagi/Downloads/chromedriver-mac-arm64/chromedriver"  # Update with your ChromeDriver path

# Streamlit App Path
STREAMLIT_APP_PATH = os.path.join(BASE_DIR, "../web/streamlit_app.py")

def main():
    print("Initializing database...") 
    create_database(DB_PATH)

    # User input
    subject = input("Enter course subject (e.g., CSE): ").strip()
    catalog_number = input("Enter course number (e.g., 505): ").strip()

    print("Step 1: Scraping courses...")
    scrape_courses(CHROME_DRIVER_PATH, subject, catalog_number, DB_PATH)

    print("Step 2: Scraping professor reviews...")
    scrape_professor_reviews(CHROME_DRIVER_PATH, DB_PATH)

    print("Step 3: Scraping faculty profiles...")
    scrape_faculty_profiles(CHROME_DRIVER_PATH, DB_PATH)

    print("Database update complete!")

    # Launch the Streamlit app
    print("Launching the Streamlit app...")
    streamlit_executable = "/Users/ashwiksagi/anaconda3/envs/asu_bot_env/bin/streamlit"  # Replace with your `streamlit` path if different
    try:
        subprocess.run([streamlit_executable, "run", STREAMLIT_APP_PATH], check=True)
    except Exception as e:
        print(f"Failed to launch Streamlit app: {e}")

if __name__ == "__main__":
    main()