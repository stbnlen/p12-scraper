import requests
from bs4 import BeautifulSoup

def get_links(soup: BeautifulSoup) -> list:
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
    top_content = sections.find("section", attrs={"class":"top-content"})
    if top_content:
        top_content_link = top_content.a.get("href")
        if top_content_link:
            links.append(f"https://www.pagina12.com.ar{top_content_link}")
    
    # Get links of the news from the content list
    list_content = sections.find("section", attrs={"class":"list-content"})
    if list_content:
        list_content_articles = list_content.find_all("article")
        for article in list_content_articles:
            article_link = article.find("a").get("href")
            if article_link:
                links.append(f"https://www.pagina12.com.ar{article_link}")
    
    return links


def get_note(url_nota: str) -> dict:
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
        if nota:
            s_nota = BeautifulSoup(nota.text, 'lxml').find("article", attrs={"class":"article-full section"})
            titulo = s_nota.find("h1").text
            fecha = s_nota.find("time").get("datetime")
            copete = s_nota.find("h2", attrs={"class":"h3"}).text
            volanta = s_nota.find("h2", attrs={"class":"h4"}).text
            tags = s_nota.find_all("a", attrs={"class": "tag"})
            body_texts = s_nota.find("div", attrs={"class": "article-main-content article-text"}).find_all("p")
            
            noticia = {
                "title": titulo,
                "date": fecha,
                "lead": copete,
                "subtitle": volanta,
                "tags": [tag.text for tag in tags],
                "body": [body_text.text for body_text in body_texts]
            }
    except Exception as e:
        print("Error:")
        print("\n")
        print(e)
    return noticia
