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

def search_top_results(query):
    response = requests.get(f"https://en.wikipedia.org/w/index.php?fulltext=1&search={query}&title=Special%3ASearch&ns0=1")

    if response.status_code != 200:
        print(Fore.RED + 'There is a problem with fetching data. Please try again!')
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Retrieve search results
    search_results_ul = soup.find('ul', class_='mw-search-results')

    if not search_results_ul:
        print(f'{Fore.RED}No results could be found for "{query}".')
        return
    
    top_results = []

    search_result_items = search_results_ul.find_all('li', class_='mw-search-result')

    # Get top 10 or less results
    for item in search_result_items[:10]:
        top_results.append(item)    

    print(f'Here are the results for: \"{query}\"')
    # Ask user which article they are looking for
    for i, item in enumerate(top_results):
        title = item.find('a').get('title').strip()
        desc = item.find('div', class_='searchresult').get_text().strip()
        print(f"{Style.BRIGHT}{i+1}. {Fore.CYAN}{title}{Fore.RESET}{Style.RESET_ALL} - {desc}\n")
        
    # Ask user what page they want    
    page_num = 1
    while True:
        page = input("Pick a page: ")
        if page.lower() == 'q':
            return None  # User wants to quit
        elif page.isdigit():
            page_num = int(page)
            if 1 <= page_num <= len(top_results):
                break
    
    search_wikipedia(top_results[page_num-1].find('a').get('title').strip())

def main():
    parser = argparse.ArgumentParser(description='Search for Wikipedia pages.')
    parser.add_argument('query', type=str, help='The Wikipedia page to search for')
    args = parser.parse_args()
    search_top_results(args.query)

if __name__ == "__main__":
    main()
