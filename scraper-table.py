import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.w3schools.com/html/html_tables.asp'  # Replace with your target URL
response = requests.get(url)
response.raise_for_status()
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table')

# Extract headers
headers = []
header_row = table.find('tr')
for th in header_row.find_all('th'):
    headers.append(th.text.strip())

# Extract rows
rows = []
for row in table.find_all('tr')[1:]:
    cells = row.find_all(['td', 'th'])
    row_data = [cell.text.strip() for cell in cells]
    rows.append(row_data)

# Write to CSV
csv_filename = 'files/output.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)
