import requests
from bs4 import BeautifulSoup

# Function to search for a topic using the Wikipedia API
def search_wikipedia(query):
    query = query.replace(' ', '_')
    # Make the API request and parse the HTML response
    response = requests.get(f"https://en.wikipedia.org/wiki/{query}")
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the main content of the page and print it in the terminal
    content = soup.find(id='mw-content-text').find_all('p')
    print('\n'.join([p.get_text() for p in content]))

query = input("Enter a topic to search for: ")
search_wikipedia(query)