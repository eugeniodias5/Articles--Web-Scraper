from selenium.webdriver.support.ui import WebDriverWait
from Scraper_Selenium import Scraper

import math, threading

class ACMDL(Scraper):
    def __init__(self):
        super().__init__(type(self).__name__)

    def return_data(self):
        xpath_num_pages = '//*[@id="pb-page-content"]/div/main/div[1]/div/div[2]/div/div[1]/div[1]/span[2]/span[1]'
        try:
            WebDriverWait(self.drivers[0], timeout=20).until(lambda d: d.find_element_by_xpath(xpath_num_pages))
        except:
            print("Tempo limite de espera excedido")
            self.drivers[-1].quit()
            exit()

        num_articles = self.drivers[0].find_element_by_xpath(xpath_num_pages).text
        num_articles = float(num_articles.replace(',', ''))
        page_size = float(self.parameters['pageSize'])
        num_pages = int(math.ceil(num_articles/page_size))
        if num_pages > self.max_pages: num_pages = self.max_pages

        #Creating a driver for each page
        self.populate_drivers(num_pages)

        threads = []
        for page in range(1, num_pages + 1):
            threads.append(threading.Thread(target=self.search_per_page, args=(page,)))

        for thread in threads:
            thread.start()
        threads[-1].join()

    def search_per_page(self, page_num = 1):
        print(f"Buscando na página {page_num}...")

        if page_num != 1:
            self.build_search({'startPage': str(page_num)}, page_num)

        page_size = int(self.parameters['pageSize'])
        for pos_article in range(1, (page_size + 1)):
            #clicking buttons to show the abstracts
            css_selector = f'"#pb-page-content > div > main > div.container > div > div.col-lg-9.col-md-9.col-sm-8.sticko__side-content > div > ul > li:nth-child({pos_article}) > div.issue-item.issue-item--search.clearfix > div.issue-item__content > div > div.issue-item__footer.clearfix > div > div.issue-item__footer-info.pull-left > ul > li.highlights-holder > div > a"'
            try:
                self.drivers[(page_num - 1)].execute_script(f'document.querySelector({css_selector}).click()')
            except:
                self.write_data(page_num, "Abstract não encontrado...")

        articles = self.drivers[(page_num - 1)].find_elements_by_class_name('issue-item')
        for article in articles:
            try:
                title = article.find_element_by_class_name('hlFld-Title')
                if title: self.write_data(data=title.text, page_num=1)
            except:
                continue

            try:
                abstract = article.find_element_by_css_selector('div.abstract-text > p')
                if abstract: self.write_data(page_num, abstract.text)
            except:
                self.write_data(page_num, "Abstract não encontrado...")

        self.drivers[(page_num - 1)].quit()
