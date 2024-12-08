from selenium import webdriver

# Initialize WebDriver
driver = webdriver.Chrome()

# Open a webpage
driver.get("https://www.google.com")

# Print the page title
print("Page title is:", driver.title)

# Close the browser
driver.quit()