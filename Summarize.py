import requests
from bs4 import BeautifulSoup                                          import openai                                                          
# Prompt user to input OpenAI API key
openai_api_key = input("Please enter your OpenAI API key: ")           openai.api_key = openai_api_key                                        
# Function to scrape data from a website
def scrape_website(url):
    response = requests.get(url)                                           soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return text
                                                                       # Function to summarize text using ChatGPT                             def summarize_text(text):
    # Create a chat completion prompt with the input text
    prompt = "summarize:\n" + text + "\nAnswer:"

    # Use OpenAI's ChatGPT API to generate the summary
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3
    )

    # Extract the summary from the API response
    summary = response.choices[0].text.strip()
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
