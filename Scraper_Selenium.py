from rich.prompt import Prompt

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


from urllib.parse import urljoin, urlencode
import json

config_name = 'config.json'

class Scraper:
    def __init__(self, name: str) -> None:
        with open(config_name, 'r') as config:
            config = json.load(config)
            config_site = config[name]
            self.url = config_site['url']
            self.parameters = config_site['parameters']
            self.max_pages = config['max_pages']
            
        self.options = Options()
        self.options.page_load_strategy = 'eager'
        #self.options.add_argument('headless')

        self.drivers = []
        self.drivers.append(Chrome('./chromedriver.exe', options=self.options))
        #Driver currently in use
        self.driver = self.drivers[-1]
        self.build_search()

    def build_search(self, attrs = {}, page_num = 1):
        for param in attrs:
            if param in self.parameters:
                self.parameters[param] = attrs[param]

        url = self.url + '?'
        for query in self.parameters:
            if self.parameters[query] == '':
                self.parameters[query] = Prompt.ask(f"Enter {query}")
            
            url += query + '=' + self.parameters[query].replace(" ", "+") + '&'
        url = url[:(len(url) - 1)]

        self.drivers[(page_num - 1)].get(url)

    #Create a driver for each page searched
    def populate_drivers(self, num_pages):
        for driver in range(num_pages - len(self.drivers)):
            self.drivers.append(Chrome('./chromedriver.exe', options=self.options))

    def write_data(self, page_num, data):
        page_num = str(page_num)
        data = str(data)

        txt = open(f"articles_page_{page_num}.txt", "a", encoding='utf-8')
        txt.write(f"{data}\n\n")
        