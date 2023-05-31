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
        print('There is a problem with fetching data. Please try again!')
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the main content of the page
    content = soup.find(id='mw-content-text').find_all('p')
    search_url = response.url
    # print("The URL we searched for is:", search_url)
    # Print only the important part of the page
    for p in content:
        if p.get_text().strip():
            print(p.get_text())
            break
    # Print the link for the full article
    print("Read more:", search_url)

print("MAKE SURE YOU'RE ENTERING VALID TOPICS THAT ARE SEARCHABLE ON WIKIPEDIA")
query = input("Enter a topic to search for: ")
search_wikipedia(query)
