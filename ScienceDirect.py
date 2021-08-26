from bs4 import BeautifulSoup

from Scraper_Requests import Scraper

class ScienceDirect(Scraper):
    def __init__(self) -> None:
        super().__init__(type(self).__name__)

    def return_data(self):
        titles = []
        soup = BeautifulSoup(self.build_search().text, 'html.parser')
        with open("teste.html", "w") as html:
            html.write(soup.prettify())

        for title in soup.find_all(class_='result-list-title-link u-font-serif text-s'):
            titles.append(title.text)
        return titles
        