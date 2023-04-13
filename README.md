# Documentation for BeautifulSoup Web Scraper for Pagina12.com.ar in Conda

This is a web scraper written in Python that uses the BeautifulSoup library to extract current news from all sections of the website Pagina12.com.ar in a Conda environment. The scraper code is designed to access the sections of the Pagina12.com.ar website, extract the title and description of the news articles, and save them in a CSV file using the Pandas library. The CSV file is saved in a folder with the date on which the scraper was run, and the file is named "news.csv".

# Requirements

To use this scraper in a Conda environment, the following requirements are needed:

Conda installed on the system.
Creation of a new Conda environment and installation of the required Python libraries using an environment.yml file provided. They can be installed using the following command:
```
conda env create -f environment.yml
conda activate my-environment
```
(replace my-environment with the name of the created environment).

# Usage
Clone the repository or download the scraper file.
Activate the Conda environment created for the scraper using the command conda activate my-environment (replace my-environment with the name of the created environment).
Open the scraper_pagina12.py file in a text editor or Python development environment.
Run the scraper_pagina12.py file using the Python interpreter from the activated Conda environment.
The scraper will access the website https://www.pagina12.com.ar, extract the current news from all sections of the website, and save them in a CSV file named "news.csv" in a folder with the date on which the scraper was run, in the directory of the scraper.
Output
The scraper saves the extracted data in a CSV file named "news.csv". The CSV file contains two columns: "Title" and "Description", which contain the title and description of the extracted news articles, respectively. The CSV file is saved in a folder with the date on which the scraper was run, in the directory of the scraper. For example, if the scraper is run on April 13, 2023, the created folder will be named "2023-04-13" and inside it, the "news.csv" file will be located.

# Limitations
This scraper is specifically designed for the Pagina12.com.ar website and may not work correctly on other websites with different HTML structures. Additionally, this scraper only extracts the title and description of the news articles. If the HTML structure of the Pagina12.com.ar website changes in the future, the scraper may stop working correctly and may require modifications to the code to adapt to the changes.