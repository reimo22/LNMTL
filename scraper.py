import requests
from bs4 import BeautifulSoup
import time
import random

# Function to extract text from the body of a webpage
def scrape_webpage(url):
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Add a random delay to avoid being detected as a bot
    time.sleep(random.uniform(1, 3))

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the body of the webpage
        body_text = soup.body.get_text(separator="\n")

        return body_text
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
if __name__ == "__main__":
    url = "https://example.com"
    text = scrape_webpage(url)
    print(text)
