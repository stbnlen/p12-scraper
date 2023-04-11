import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from functions import get_note, get_links
from datetime import datetime

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Create a folder with the current date if it doesn't exist
if not os.path.exists(current_date):
    os.makedirs(current_date)

url = "https://www.pagina12.com.ar"
p12 = requests.get(url)
p12.raise_for_status()
soup = BeautifulSoup(p12.text, "lxml")

# Get news sections
sections = soup.find('div', attrs={"class": "p12-dropdown-column"}).find_all("a")

# Get links of news sections and exclude specific elements
link_sections = [section.get("href") for section in sections if section.get("href") not in ['https://www.pagina12.com.ar/suplementos/rosario12', 'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos', 'https://www.pagina12.com.ar//buenos-aires12', 'https://www.pagina12.com.ar/edicion-impresa']]

news_list = []

# Get news links from each news section
for link_section in link_sections:
    r = requests.get(link_section)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    
    # Get news links
    news_links = get_links(soup)
    
    # Add news links to the list
    news_list.extend(news_links)

# Get news details in a single call
news_data = [get_note(url) for url in news_list]

# Create DataFrame
df = pd.DataFrame(news_data)

# Drop rows with null values
df = df.dropna()

# Save DataFrame to a CSV file in the folder with the current date
df.to_csv(f"{current_date}/news.csv", index=False)
