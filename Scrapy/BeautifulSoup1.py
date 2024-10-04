import json
from bs4 import BeautifulSoup
import requests
import os

# Scrape the website
website = 'https://subslikescript.com/movie/Titanic-120338'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Locate the data
box = soup.find('article', class_='main-article')
title = box.find('h1').get_text()
transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

# Save the scraped data in a JSON file in the specified directory
scraped_data = {
    "title": title,
    "transcript": transcript
}

# Specify the directory for the Python file
json_file_path = r'C:\Users\YanivIdov\anaconda3\envs\Scrapy\scraped_data.json'

# Write the data to the JSON file
with open(json_file_path, 'w') as file:
    json.dump(scraped_data, file)

print(f"JSON file saved at: {json_file_path}")
