import hashlib
import json
import os
import requests
from bs4 import BeautifulSoup
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

cache_filename = 'api_cache.json'
feedback_filename = 'feedback.json'   # new line

# Function to scrape data from a website
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return text

# Function to summarize text using ChatGPT
def summarize_text(text):
    # ... rest of your code ...

# Prompt user for the website URL
website_url = input("Please enter the URL of the website you want to scrape data from: ")

# Scrape the website for data
website_text = scrape_website(website_url)

# Summarize the scraped text
summary_text = summarize_text(website_text)

# Print the summary
print("\nSummary:")
print(summary_text)

# Ask for user feedback
feedback = input("\nCould you please provide some feedback for this session? It will help us improve: ")

# Save feedback
if os.path.exists(feedback_filename):
    with open(feedback_filename, 'r') as f:
        feedback_data = json.load(f)
else:
    feedback_data = {}

# Assuming each feedback is unique, you can use a timestamp as an ID
from datetime import datetime
feedback_id = datetime.now().strftime("%Y%m%d%H%M%S")
feedback_data[feedback_id] = feedback

with open(feedback_filename, 'w') as f:
    json.dump(feedback_data, f)
