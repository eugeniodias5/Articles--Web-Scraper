from requests.sessions import session
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

    def build_search(self):
        for param_val in self.parameters:
            if self.parameters[param_val] == '':
                self.parameters[param_val] = Prompt.ask(f"Enter {param_val}")
        
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'}
        #print(requests.get(self.url, params=dict(self.parameters)).url)
        self.url += '?'
        for parameter in self.parameters:
            self.url += f'{parameter}={self.parameters[parameter]}&'
        
        requests.post(self.url,  allow_redirects=True)
        #return requests.get(self.url,  allow_redirects=True, cookies= {'idp_session': 'idp_session=sVERSION_1e626a09a-df7e-4829-b741-ad4b5194e988'})
        session = requests.Session()
        #Getting cookie
        session.get(self.url)
        #Sending the result
        return session.get(self.url)
        
    def write_data(self, page_num, data):
        page_num = str(page_num)
        data = str(data)

        txt = open(f"articles_page_{page_num}.txt", "a", encoding='utf-8')
        txt.write(f"{data}\n\n")
