from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time

#https://googlechromelabs.github.io/chrome-for-testing/#stable

# Specify path to ChromeDriver
service = Service('/opt/homebrew/bin/chromedriver')  # Update with your ChromeDriver path Linux: /usr/bin/chromedriver

# Initialize ChromeDriver with Service
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox")  # Recommended for headless mode
options.add_argument("--disable-dev-shm-usage")  # Recommended to prevent memory issues in headless mode

# Initialize WebDriver with headless options
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Access login page and authenticate
url = 'http://frontend-stage.tasso-project.eu/login?returnUrl=%2F'
driver.get(url)

time.sleep(2)

# Locate and input credentials
username = driver.find_element(By.ID, "username")  # Update with actual input name
password = driver.find_element(By.ID, "password")  # Update with actual input name

username.send_keys("your_username")  # Replace with your username
password.send_keys("your_password")  # Replace with your password
#password.send_keys(Keys.RETURN)  # Submit login form
submit_button = driver.find_element(By.CSS_SELECTOR, "button.p-button.p-component[ng-reflect-label='Submit']")
submit_button.click()

# Step 2: Wait for redirection or use WebDriverWait for more precise control
time.sleep(2)

gestione_processi_button = driver.find_element(By.CSS_SELECTOR, "button.p-button-raised.p-button-text.p-button[ng-reflect-label='Gestione processi']")
gestione_processi_button.click()

time.sleep(2)

table_div = driver.find_element(By.CLASS_NAME, "p-datatable-scrollable-view")

# Extract rows and columns
rows = table_div.find_elements(By.CSS_SELECTOR, "table tbody tr")
data = []

# Loop through rows and collect data
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    row_data = [cell.text.strip() for cell in cells]
    data.append(row_data)

# Step 4: Save to CSV
csv_filename = "data/table_data.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Step 4: Close the browser
driver.quit()
