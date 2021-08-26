import requests, csv, threading

from bs4 import BeautifulSoup
from Scraper_Requests import Scraper

config = 'config.json'
threads_max = 4

class Springer(Scraper):
    def __init__(self):
        super().__init__(type(self).__name__)
        
    def return_data(self):
        #First download CSV with articles data and URLs for articles
        download = self.build_search()      
        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines())
        my_list = list(cr)

        threads = []
        for thread_index in range(threads_max):
            threads.append(threading.Thread(target=self.thread_search, args=(my_list[1:], thread_index)))

        for thread in threads:
            thread.start()

        threads[-1].join()

    def thread_search(self, csv_list, thread_num):
        print(f'Thread {thread_num+1} searching for articles...')
        session = requests.session()
        #Setting cookie
        session.get(self.url)
        for row_ind in range(thread_num, len(csv_list), threads_max):
            row = csv_list[row_ind]
            self.write_data(thread_num, row[0])

            article_url = row[8]
            soup = BeautifulSoup(session.get(url=article_url).text, 'html.parser')
            abstract = soup.select('#Abs1-content > p')
            
            if abstract:
                self.write_data(thread_num+1, abstract[0].getText())
            else: 
                self.write_data(thread_num+1, "Abstract not found")
