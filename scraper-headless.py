from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
from logging.handlers import TimedRotatingFileHandler
import csv
import time

# Set up daily log rotation
log_handler = TimedRotatingFileHandler(
    "log/main.log",         # Base log file name
    when="midnight",      # Rotate at midnight
    interval=1,           # Rotate every 1 day
    backupCount=7         # Keep logs for the last 7 days
)
log_handler.suffix = "%Y-%m-%d"  # Log file names will include the date

# Set up logging format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)

# Configure the root logger to use the rotating handler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

try:
    logging.info("Starting the Selenium script")

    # Set up ChromeDriver service and options
    # Specify path to ChromeDriver
    service = Service('/opt/homebrew/bin/chromedriver')  # Update with your ChromeDriver path Linux: /usr/bin/chromedriver

    # Initialize ChromeDriver with Service
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver with headless options
    driver = webdriver.Chrome(service=service, options=options)
    logging.info("Chrome WebDriver initialized")

    # Step 1: Access the login page and log in
    url = 'http://frontend-stage.tasso-project.eu/'
    driver.get(url)
    logging.info(f"Accessed URL: {url}")

    username = driver.find_element(By.ID, "username")  # Update with actual input name
    password = driver.find_element(By.ID, "password")  # Update with actual input name

    username.send_keys("admin")
    password.send_keys("B3ll4v1t4!")
    logging.info("Entered username and password")

    # Click the submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, "button.p-button.p-component[ng-reflect-label='Submit']")
    submit_button.click()
    logging.info("Clicked the submit button")

    # Wait for redirection or page load
    time.sleep(3)

    # Step 2: Click the "Gestione processi" button
    gestione_processi_button = driver.find_element(By.CSS_SELECTOR, "button.p-button-raised.p-button-text.p-button[ng-reflect-label='Gestione processi']")
    gestione_processi_button.click()
    logging.info("Clicked the 'Gestione processi' button")

    # Wait for the table to load
    time.sleep(3)

    # Step 3: Locate the table within the div "p-datatable-scrollable-view"
    table_div = driver.find_element(By.CLASS_NAME, "p-datatable-scrollable-view")
    logging.info("Located the table div")

    # Extract rows and columns
    rows = table_div.find_elements(By.CSS_SELECTOR, "table tbody tr")
    data = []

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)
    logging.info("Extracted table data")

    # Step 4: Save to CSV
    csv_filename = "data/table_data.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    logging.info(f"Data saved to {csv_filename}")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    # Step 5: Close the driver
    driver.quit()
    logging.info("Closed the WebDriver and finished script")
