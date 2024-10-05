import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the WebDriver (automatically downloads the required driver)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Booking.com page
url = "https://www.booking.com/searchresults.en-US.html?dest_type=hotel&dest_id=4480704&checkin=2021-2-1;checkout=2021-2-2&selected_currency=USD;"
driver.get(url)

# Initialize WebDriverWait
wait = WebDriverWait(driver, 10)

# Scroll and load more hotels until we reach the bottom of the page
scroll_pause_time = 3
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the new hotels to load
    time.sleep(scroll_pause_time)

    # Calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # If heights are the same, exit the loop
    last_height = new_height

# Now scrape all the property cards
property_cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='property-card']")))

# Prepare data to store in JSON format
ranking_data = []

# Loop through each property card to extract the ranking (review score) and hotel name
for card in property_cards:
    try:
        # Extract the hotel name
        hotel_name = card.find_element(By.XPATH, ".//div[@data-testid='title']").text

        # Extract the review score (rating) if available
        review_score_element = card.find_elements(By.XPATH,
                                                  ".//div[@data-testid='review-score']//div[contains(@class, 'a3b8729ab1')]")
        if review_score_element:
            # Extract the score (e.g., "Scored 8.5") and clean it up
            review_score = review_score_element[0].text.split("\n")[0]
        else:
            review_score = "No rating"

        # Append the data to the list
        ranking_data.append({
            "hotel_name": hotel_name,
            "rating": review_score  # Use only the first part of the score
        })
    except Exception as e:
        # If any exception occurs, print it and continue
        print(f"Error extracting data for a hotel: {e}")
        continue

# Write the rankings to a JSON file
with open('ranking.json', 'w') as json_file:
    json.dump(ranking_data, json_file, indent=4)

# Close the WebDriver
driver.quit()

print("Rankings have been saved to ranking.json")
