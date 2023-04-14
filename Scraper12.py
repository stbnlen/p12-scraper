import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict, Any

class Pagina12Scraper:
    def __init__(self, base_url: str):
        """
        Constructor for Pagina12Scraper class.

        Args:
            base_url (str): Base URL of the webpage to scrape.
        """
        self.base_url = base_url

    def get_link_sections(self) -> list:
        """
        Get the links of the news sections from the webpage.

        Returns:
            list: List of links of the news sections.
        """
        # Get the content of the webpage
        response = requests.get(self.base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Get news sections
        sections = soup.find(
            'div', attrs={"class": "p12-dropdown-column"}).find_all("a")

        # Get links of news sections and exclude specific elements
        link_sections = [section.get("href") for section in sections if section.get("href") not in ['https://www.pagina12.com.ar/suplementos/rosario12', 'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                                                                                                    'https://www.pagina12.com.ar//buenos-aires12', 'https://www.pagina12.com.ar/edicion-impresa', 'https://www.pagina12.com.ar//suplementos/soy', 'https://www.pagina12.com.ar//suplementos/las12']]

        return link_sections

    def get_links(self, soup: BeautifulSoup) -> list:
        """
        Get the links of the news from a web page.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of the web page.

        Returns:
            list: List of links of the news.
        """
        links = []
        sections = soup.find('div', attrs={"class": "main-content"})

        # Get link of the featured news
        top_content = sections.find("section", attrs={"class": "top-content"})
        if top_content:
            top_content_link = top_content.a.get("href")
            if top_content_link:
                links.append(f"{self.base_url}{top_content_link}")

        # Get links of the news from the content list
        list_content = sections.find(
            "section", attrs={"class": "list-content"})
        if list_content:
            list_content_articles = list_content.find_all("article")
            for article in list_content_articles:
                article_link = article.find("a").get("href")
                if article_link:
                    links.append(f"{self.base_url}{article_link}")

        return links

    def get_note(self, url_nota: str) -> dict:
        """
        Get the details of a news article from its URL.

        Args:
            url_nota (str): URL of the news article.

        Returns:
            dict: Dictionary with the details of the news article, including title,
                  date, lead, subtitle, tags, and body content of the news article.
        """
        noticia = {}
        try:
            nota = requests.get(url_nota)
            nota.raise_for_status()  # Raise an exception if the request returns an error status code
            s_nota = BeautifulSoup(nota.text, 'lxml').find(
                "article", attrs={"class": "article-full section"})
            titulo = s_nota.find("h1").text
            fecha = s_nota.find("time").get("datetime")
            copete = s_nota.find("h2", attrs={"class": "h3"}).text
            volanta = s_nota.find("h2", attrs={"class": "h4"}).text
            tags = s_nota.find_all("a", attrs={"class": "tag"})
            body_texts = s_nota.find(
                "div", attrs={"class": "article-main-content article-text"}).find_all("p")

            noticia = {
                "title": titulo,
                "date": fecha,
                "lead": copete,
                "subtitle": volanta,
                "tags": [tag.text for tag in tags],
                "body": [body_text.text for body_text in body_texts]
            }
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
        except Exception as e:
            print("Error:")
            print(e)
        return noticia
    

    def create_dataframe(self, news_data: List[Dict[str, Any]], current_date: str) -> None:
        """
        Create a Pandas DataFrame from a list of dictionaries containing news data and save it to a CSV file.

        Args:
            news_data (List[Dict[str, Any]]): List of dictionaries containing news data.
            current_date (str): Current date in the format '%Y-%m-%d'.

        Returns:
            None
        """
        # Create DataFrame from list of dictionaries
        df = pd.DataFrame(news_data)

        # Drop rows with null values
        df.dropna(inplace=True)

        # Save DataFrame to a CSV file in the folder with the current date
        df.to_csv(f"{current_date}/news.csv", index=False)
