import argparse
import os
import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# Initialize Colorama for Windows compatibility
init()

API_KEY_FILE = 'api_key.txt'


# Function to save API key to a file
def save_api_key(api_key):
    with open(API_KEY_FILE, 'w') as file:
        file.write(api_key)


# Function to load API key from a file
def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as file:
            return file.read().strip()
    return None


# Initialize Gemini AI model
def initialize_gemini_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')


# Function to clean references from text
def clean_references(text):
    return re.sub(r'\[\d+\]', '', text)


# Function to search Wikipedia
def search_wikipedia(query):
    query = query.replace(' ', '_')
    try:
        response = requests.get(f"https://en.wikipedia.org/wiki/{query}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(Fore.RED + 'Wikipedia does not have an article with this exact name.')
        else:
            print(Fore.RED + f'HTTP error occurred: {http_err}')
        return
    except requests.exceptions.RequestException as err:
        print(Fore.RED + f'Error occurred: {err}')
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract and display the info box if present
    infobox = soup.find('table', class_='infobox')
    if infobox:
        infobox_rows = infobox.find_all('tr')
        for row in infobox_rows:
            if row.th and row.td:
                header_text = clean_references(row.th.get_text().strip())
                data_text = clean_references(row.td.get_text().strip())
                print(f"{Style.BRIGHT}{header_text}{Style.RESET_ALL}: {data_text}")

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


# Function to search for top results on Wikipedia
def search_top_results(query):
    try:
        response = requests.get(
            f"https://en.wikipedia.org/w/index.php?fulltext=1&search={query}&title=Special%3ASearch&ns0=1")
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(Fore.RED + f'Error occurred: {err}')
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
        print(f"{Style.BRIGHT}{i + 1}. {Fore.CYAN}{title}{Fore.RESET}{Style.RESET_ALL} - {clean_references(desc)}\n")

    # Ask user which article they want
    while True:
        page = input("Pick a page: ")
        if page.lower() == 'q':
            return  # User wants to quit
        elif page.isdigit() and 1 <= int(page) <= len(top_results):
            search_wikipedia(top_results[int(page) - 1].find('a').get('title').strip())
            break
        else:
            print(Fore.RED + "Invalid input, please try again.")


# Function to interact with Gemini AI
def interact_with_gemini(model):
    while True:
        user_input = input(">> ")
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
        try:
            response = model.generate_content(user_input)
            print(response.text)
        except GoogleAPIError as api_err:
            print(Fore.RED + f"Google API error occurred: {api_err}")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description='Search for Wikipedia pages and interact with Gemini AI.')
    parser.add_argument('query', nargs='?', type=str, help='The Wikipedia page to search for')
    parser.add_argument('-gai', action='store_true', help='Give the query to Gemini AI and get a response')
    parser.add_argument('--gai', action='store_true', help='Enter continuous prompt mode to interact\
     with Gemini AI')

    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
        save_api_key(api_key)

    # Initialize Gemini AI model
    gemini_model = initialize_gemini_ai(api_key)

    if args.gai and args.query:
        try:
            response = gemini_model.generate_content(args.query)
            print(response.text)
        except GoogleAPIError as api_err:
            print(Fore.RED + f"Google API error occurred: {api_err}")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
    elif args.gai:
        interact_with_gemini(gemini_model)
    elif args.query:
        search_top_results(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
