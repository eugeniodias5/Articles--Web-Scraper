import requests
from rich.prompt import Prompt
from bs4 import BeautifulSoup

from Scraper import Scraper

config = 'config.json'

class IEEE(Scraper):
    def __init__(self):
        super().__init__(type(self).__name__)

    def build_search_query(self):
        for param_val in self.parameters:
            if self.parameters[param_val] == '':
                self.parameters[param_val] = Prompt.ask(f"Enter {param_val}")

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://ieeexplore.ieee.org",
            "Content-Type": "application/json",
        }
        payload = {
            "newsearch": True,
            "queryText": self.parameters["queryText"],
            "highlight": True,
            "returnFacets": ["ALL"],
            "returnType": "SEARCH",
        }
        r = requests.post(
                "https://ieeexplore.ieee.org/rest/search",
                json=payload,
                headers=headers
            )
        page_data = r.json()
        return page_data["records"]

    def return_titles(self):
        titles = []
        for record in self.build_search_query():
            titles.append(record["articleTitle"])

        return titles
