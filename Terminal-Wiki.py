# This is a test comment
import requests
from bs4 import BeautifulSoup

# Function to search for a topic using the Wikipedia API
def search_wikipedia(query):
    query = query.replace(' ', '_')
    # Make the API request and parse the HTML response
    response = requests.get(f"https://en.wikipedia.org/wiki/{query}")
    if response.status_code == 404:
        print('Wikipedia does not have an article with this exact name.')
        return
    elif response.status_code != 200:
        print('There is a problem with fetching data. please try again!')
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the main content of the page and print it in the terminal
    content = soup.find(id='mw-content-text').find_all('p')
    search_url = response.url
    print("the url we searched for is: ", search_url)
    print('\n'.join([p.get_text() for p in content]))

print("MAKE SURE YOU'RE ENTERING VALID TOPICS THAT ARE SEARCHABLE ON WIKIPEDIA")
query = input("Enter a topic to search for: ")
search_wikipedia(query)