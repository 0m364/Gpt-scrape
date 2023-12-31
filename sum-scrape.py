import hashlib
import json
import os
import requests
from bs4 import BeautifulSoup
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

cache_filename = 'api_cache.json'

# Function to scrape data from a website
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return text

# Function to summarize text using ChatGPT
def summarize_text(text):
    # Create a chat completion prompt with the input text
    prompt = "summarize:\n" + text + "\nAnswer:"

    # Create a hash of the prompt
    text_hash = hashlib.sha256(prompt.encode()).hexdigest()

    # Check if the hash exists in the cache
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r') as f:
            cache = json.load(f)
            if text_hash in cache:
                return cache[text_hash]

    # If it doesn't exist in the cache, use OpenAI's ChatGPT API to generate the summary
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.3
    )

    # Extract the summary from the API response
    summary = response.choices[0].text.strip()

    # Store the summary in the cache
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r') as f:
            cache = json.load(f)
    else:
        cache = {}

    cache[text_hash] = summary
    with open(cache_filename, 'w') as f:
        json.dump(cache, f)

    return summary

# Prompt user for the website URL
website_url = input("Please enter the URL of the website you want to scrape data from: ")

# Scrape the website for data
website_text = scrape_website(website_url)

# Summarize the scraped text
summary_text = summarize_text(website_text)

# Print the summary
print("\nSummary:")
print(summary_text)
