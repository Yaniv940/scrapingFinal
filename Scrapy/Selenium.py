import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the Booking.com search results page
url = "https://www.booking.com/searchresults.en-US.html?dest_type=hotel&dest_id=4480704&checkin=2021-2-1;checkout=2021-2-2&selected_currency=USD;"
driver.get(url)

# Wait until property cards are present
wait = WebDriverWait(driver, 10)

# Scroll and load more hotels until we reach the bottom of the page
scroll_pause_time = 3
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # If heights are the same, exit the loop
    last_height = new_height

# Get all property cards
property_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='property-card']")))

# Prepare an empty list to store the ranking data
ranking_data = []

# Iterate over each property card to extract data
for card in property_cards:
    try:
        # Extract hotel name
        hotel_name_element = card.find_element(By.CSS_SELECTOR, "div[data-testid='title']")
        hotel_name = hotel_name_element.text if hotel_name_element else "No name"

        # Extract review score (if available)
        review_score_element = card.find_elements(By.CSS_SELECTOR, "div[data-testid='review-score'] div[class*='a3b8729ab1']")
        review_score = review_score_element[0].text.split("\n")[0] if review_score_element else "No rating"

        # Append hotel name and review score to the ranking data
        ranking_data.append({
            "hotel_name": hotel_name,
            "rating": review_score
        })

    except Exception as e:
        print(f"Error extracting data for a hotel: {e}")
        continue

# Save the data to a JSON file
with open('ranking.json', 'w') as json_file:
    json.dump(ranking_data, json_file, indent=4)

# Close the driver
driver.quit()

# Output success message
print("Rankings have been saved to ranking.json")
