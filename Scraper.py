from rich.prompt import Prompt
import requests
import json

config_name = 'config.json'

class Scraper:
    def __init__(self, name: str) -> None:
        with open(config_name, 'r') as config:
            config = json.load(config)[name]
            self.url = config['url']
            self.parameters = config['parameters']

    def build_search_query(self):
        for param_val in self.parameters:
            if self.parameters[param_val] == '':
                self.parameters[param_val] = Prompt.ask(f"Enter {param_val}")
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'}
        return requests.get(self.url, params=self.parameters, headers=headers, allow_redirects=True)
