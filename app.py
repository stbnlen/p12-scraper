import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from Scraper12 import Pagina12Scraper


def main():
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create a folder with the current date if it doesn't exist
    if not os.path.exists(current_date):
        os.makedirs(current_date)

    # URL of the webpage to scrape
    URL = "https://www.pagina12.com.ar"

    # Create an instance of Pagina12Scraper
    scraper = Pagina12Scraper(URL)

    # Get links of news sections and exclude specific elements
    link_sections = scraper.get_link_sections()

    # List to store news links
    news_list = []

    # Get news links from each link section
    for link_section in link_sections:
        try:
            r = requests.get(link_section)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "lxml")
            # Get news links
            news_links = scraper.get_links(soup)
            # Add news links to the list
            news_list.extend(news_links)
        except requests.exceptions.HTTPError as e:
            print(
                f'Error getting news links from section {link_section}: {e}')
        except Exception as e:
            print(
                f'General error getting news links from section {link_section}: {e}')

    # Get news details in a single call
    news_data = []
    for url in news_list:
        try:
            news_data.append(scraper.get_note(url))
        except Exception as e:
            print(
                f'Error getting news details from URL {url}: {e}')

    scraper.create_dataframe(news_data, current_date)

if __name__ == '__main__':
    main()
