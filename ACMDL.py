from bs4 import BeautifulSoup
from Scraper import Scraper

config = 'config.json'

class ACMDL(Scraper):
    def __init__(self):
        super().__init__(type(self).__name__)
        
    def return_titles(self):
        titles = []
        soup = BeautifulSoup(self.build_search_query().text, 'html.parser')
        for title in soup.find_all(class_='hlFld-Title'):
            titles.append(title.text)
        return titles