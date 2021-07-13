from bs4 import BeautifulSoup
from Scraper import Scraper

config = 'config.json'

class Springer(Scraper):
    def __init__(self):
        super().__init__(type(self).__name__)
        
    def return_data(self):
        #First download CSV with articles data and URLs for articles
        titles = []
        soup = BeautifulSoup(self.build_search_query().text, 'html.parser')
        for title in soup.find_all(class_='title'):
            titles.append(title.text)
        return titles
