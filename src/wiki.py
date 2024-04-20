import argparse
import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore, Style

def clean_references(text):
    # Use regular expressions to remove references, e.g., [1], [2], etc.
    return re.sub(r'\[\d+\]', '', text)

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

    # Extract and display the info box if present
    infobox = soup.find('table', class_='infobox')
    if infobox:
        print(Style.BRIGHT + clean_references(infobox.get_text(separator='\n', strip=True)) + Style.RESET_ALL + '\n')

    # Extract the first few paragraphs
    content = soup.find(id='mw-content-text').find_all('p')
    search_url = response.url
    print(Style.RESET_ALL + "Summary:")
    for i, p in enumerate(content):
        if i >= 3:  # Limit to first 3 paragraphs
            break
        cleaned_text = clean_references(p.get_text().strip())
        if cleaned_text:
            print(cleaned_text)

    print(Fore.BLUE + "Read more:", search_url)

def search_top_results(query):
    response = requests.get(f"https://en.wikipedia.org/w/index.php?fulltext=1&search={query}&title=Special%3ASearch&ns0=1")

    if response.status_code != 200:
        print(Fore.RED + 'There is a problem with fetching data. Please try again!')
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    search_results_ul = soup.find('ul', class_='mw-search-results')
    if not search_results_ul:
        print(f'{Fore.RED}No results could be found for "{query}".')
        return

    top_results = search_results_ul.find_all('li', class_='mw-search-result', limit=10)

    print(f'Here are the results for: \"{query}\"')
    for i, item in enumerate(top_results):
        title = item.find('a').get('title').strip()
        desc = item.find('div', class_='searchresult').get_text().strip()
        print(f"{Style.BRIGHT}{i+1}. {Fore.CYAN}{title}{Fore.RESET}{Style.RESET_ALL} - {clean_references(desc)}\n")

    # Ask user which article they want
    while True:
        page = input("Pick a page: ")
        if page.lower() == 'q':
            return  # User wants to quit
        elif page.isdigit() and 1 <= int(page) <= len(top_results):
            search_wikipedia(top_results[int(page)-1].find('a').get('title').strip())
            break
        else:
            print(Fore.RED + "Invalid input, please try again.")

def main():
    parser = argparse.ArgumentParser(description='Search for Wikipedia pages.')
    parser.add_argument('query', type=str, help='The Wikipedia page to search for')
    args = parser.parse_args()
    search_top_results(args.query)

if __name__ == "__main__":
    main()
