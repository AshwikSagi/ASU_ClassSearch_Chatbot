# ASU Class Search Virtual Assistant

A powerful, intuitive web application that consolidates and simplifies the search for class and faculty information at Arizona State University. This project leverages Python, SQL, and Streamlit to provide students with an interactive tool to explore courses, instructor profiles, and reviews.

## Table of Contents
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Problem Statement

Students often face challenges when searching for class and instructor information:
- Course and faculty data is scattered across multiple platforms
- Lack of centralized access to professor reviews and course details
- Time-consuming manual searches for relevant information

This project solves these problems by creating a single platform to access and query all relevant information.

## Features
- **Centralized Database**: Consolidates course, instructor, and review data
- **Interactive Web App**: Built with Streamlit, allowing users to search, filter, and query information
- **Custom SQL Query Execution**: Supports advanced queries directly from the interface
- **Data Scraping**: Automatically fetches and updates course, faculty, and review information
- **User-Friendly Interface**: Intuitive design for quick and easy access to data

## Technologies Used
- **Python**: Core programming language for data scraping and backend logic
- **SQL (SQLite)**: For database management and custom queries
- **Streamlit**: Framework for creating the interactive web application
- **Selenium**: For automating data scraping tasks
- **BeautifulSoup**: For parsing HTML content during scraping
- **Pandas**: For data processing and analysis

## System Architecture
1. **Scraping Layer**: Extracts data from ASU's course catalog, Rate My Professors, and faculty directories using Selenium and BeautifulSoup
2. **Database Layer**: Stores scraped data in an SQLite database
3. **Frontend Layer**: Displays course and instructor information through a Streamlit-based interface

## Setup Instructions

### Prerequisites
- Python 3.9 or later
- SQLite
- Google Chrome and ChromeDriver (for Selenium)

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/AshwikSagi/ASU_ClassSearch_Chatbot.git
cd ASU_ClassSearch_Chatbot
```

2. **Create a Virtual Environment**
```bash
python -m venv asu_bot_env
source asu_bot_env/bin/activate   # On Windows: asu_bot_env\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up the Database**
Run the main.py script to initialize the database:
```bash
python src/main.py
```

5. **Run the Streamlit Application**
After the database is set up, the Streamlit app will launch automatically. Alternatively, you can run it manually:
```bash
streamlit run web/streamlit_app.py
```

## Usage

### Searching for a Course
1. Launch the Streamlit app
2. Enter the course subject (e.g., CSE) and course number (e.g., 510) to retrieve detailed course and instructor information

### Executing Custom Queries
- Use the custom query feature in the app to run SQL queries and extract specific insights

## Future Enhancements
- **GPT Assistant**: Add AI-powered natural language querying to make SQL execution more intuitive
- **Data Visualizations**: Include graphical representations of course trends and reviews
- **Multi-University Support**: Expand the database to cover other universities
- **Automated Scheduling**: Enable integration with student schedules for better course planning

## Contributing

We welcome contributions to improve this project!

1. Fork the repository
2. Create a new branch for your feature or bug fix:
```bash
git checkout -b feature-name
```

3. Commit your changes and push to your branch:
```bash
git commit -m "Description of your changes"
git push origin feature-name
```

4. Create a pull request

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)










