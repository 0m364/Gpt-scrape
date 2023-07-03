
import hashlib
import json
import os
import requests
import sqlite3
from bs4 import BeautifulSoup
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

cache_filename = 'api_cache.json'

# Connect to the database or create a new one if it doesn't exist
conn = sqlite3.connect('website_data.db')
cursor = conn.cursor()

# Create a table for storing website data if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS website_info
                  (url TEXT, md5_hash TEXT, summary TEXT)''')

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

add_more_sites = True

while add_more_sites:
    # Get website URL from the user
    url = input("Enter a website URL: ")

    # Scrape the website for data
    website_text = scrape_website(url)

    # Calculate MD5 hash of the website content
    md5_hash = hashlib.md5(website_text.encode()).hexdigest()

    # Summarize the scraped text
    summary_text = summarize_text(website_text)

    # Print summary in terminal
    print(f"Website URL: {url}")
    print(f"MD5 Hash: {md5_hash}")
    print("\nSummary:")
    print(summary_text)

    # Insert website information into the database
    cursor.execute("INSERT INTO website_info VALUES (?, ?, ?)", (url, md5_hash, summary_text))
    conn.commit()

    # Ask if the user wants to add more sites
    add_more = input("Do you want to add more sites? (yes/no): ")
    add_more = add_more.lower()

    if add_more != 'yes':
        add_more_sites = False

# Close the database connection
conn.close()
