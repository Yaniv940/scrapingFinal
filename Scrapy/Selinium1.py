from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import json
import os

# define the website to scrape
website = 'https://www.adamchoi.co.uk/overs/detailed'

# Automatically download and manage the ChromeDriver using webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# open Google Chrome with chromedriver
driver.get(website)

# Explicitly wait until the "All matches" button is available before clicking
try:
    all_matches_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//label[@analytics-event="All matches"]'))
    )
    all_matches_button.click()
except Exception as e:
    print(f"Error: {e}")

# select elements in the table
matches = driver.find_elements(By.XPATH, '//tr')

# storage data in lists
date = []
home_team = []
score = []
away_team = []

# looping through the matches list
for match in matches:
    try:
        # Ensure the row has the expected number of columns before extracting
        columns = match.find_elements(By.XPATH, './td')
        if len(columns) == 4:  # Check if the row contains 4 columns
            date.append(columns[0].text)
            home = columns[1].text
            home_team.append(home)
            print(home)
            score.append(columns[2].text)
            away_team.append(columns[3].text)
        else:
            print("Skipping row with unexpected number of columns")
    except Exception as e:
        print(f"Error processing row: {e}")

# quit driver
driver.quit()

# Create Dataframe in Pandas
df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})

# Convert DataFrame to JSON format and save to a file
json_data = df.to_json(orient='records', indent=4)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, 'football_data.json')

# Save the JSON data to a file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print(f"Data saved to: {json_file_path}")
