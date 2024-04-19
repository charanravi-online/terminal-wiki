import argparse
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def search_wikipedia(query):
    query = query.replace(' ', '_')
    response = requests.get(f"https://en.wikipedia.org/wiki/{query}")
    if response.status_code == 404:
        print(Fore.RED + 'Wikipedia does not have an article with this exact name.')
        return
    elif response.status_code != 200:
        print(Fore.RED + 'There is a problem with fetching data. Please try again!')
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find(id='mw-content-text').find_all('p')
    search_url = response.url
    for p in content:
        if p.get_text().strip():
            print(Style.RESET_ALL + p.get_text())
            break
    print(Fore.BLUE + "Read more:", search_url)

def main():
    parser = argparse.ArgumentParser(description='Search for Wikipedia pages.')
    parser.add_argument('query', type=str, help='The Wikipedia page to search for')
    args = parser.parse_args()
    search_wikipedia(args.query)

if __name__ == "__main__":
    main()
