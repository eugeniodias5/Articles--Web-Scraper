from bs4 import BeautifulSoup

from Scraper import Scraper

class ScienceDirect(Scraper):
    def __init__(self) -> None:
        super().__init__(type(self).__name__)

    def return_titles(self):
        titles = []
        soup = BeautifulSoup(self.build_search_query().text, 'html.parser')
        for title in soup.find_all(class_='result-list-title-link u-font-serif text-s'):
            titles.append(title.text)
        return titles
        