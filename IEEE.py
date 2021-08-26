from selenium.webdriver.support.ui import WebDriverWait
import math

import threading

from Scraper_Selenium import Scraper

class IEEE(Scraper):
    def __init__(self):
        super().__init__(type(self).__name__)

    def return_data(self):
        try:
            WebDriverWait(self.drivers[0], timeout=20).until(lambda d: d.find_elements_by_class_name("List-results-items"))
        except:
            print("Tempo limite de espera excedido")
            self.drivers[-1].quit()
            exit()

        rows_per_page = int(self.parameters['rowsPerPage'])
        total_articles = self.drivers[0].find_element_by_xpath('//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/div[1]/span[1]/span[2]').text
        total_articles = total_articles.replace(',', '')
        num_pages = math.ceil(float(total_articles)/float(rows_per_page))
        if num_pages > self.max_pages: num_pages = self.max_pages

        #Creating a driver for each page
        self.populate_drivers(num_pages)

        threads = []
        for page in range(1, num_pages + 1):
            threads.append(threading.Thread(target=self.search_per_page, args=(page,)))

        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()

    def search_per_page(self, page_num):
        print(f"Buscando na página {page_num}...")
        articles = []

        self.build_search({'pageNumber': str(page_num - 1)}, (page_num - 1))
    
        try:    
            articles_search = WebDriverWait(self.drivers[(page_num - 1)], timeout=50).until(lambda d: d.find_elements_by_class_name("List-results-items"))
            articles = articles_search
        except:
            print(f"Não foi possível a busca na página {page_num}, tempo de espera excedido.")
            self.drivers[(page_num - 1)].quit()
            exit()

        for article in articles:
            try:
                article_id = article.get_attribute("id")
                xpath = f'//*[@id=\'{article_id}\']/xpl-results-item/div[1]/div[2]/ul/li[1]/a'
                js_command = f'document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();'
                
                self.drivers[(page_num - 1)].execute_script(js_command)
            except:
                #print("Não foi possível abrir abstract...")
                pass

        for article in articles:
            try:
                article_id = article.get_attribute("id")
                title_xpath = f"//*[@id=\'{article_id}\']/xpl-results-item/div[1]/div[1]/div[2]/h2/a"
                title = article.find_element_by_xpath(title_xpath).text
                self.write_data(page_num, title)
            except:
                self.write_data(page_num, "Título não encontrado...")
                continue

            abstract_xpath = f"//*[@id=\'{article_id}\']/xpl-results-item/div[1]/div[2]/div/span"
            try:
                abstract = article.find_element_by_xpath(abstract_xpath).text
                self.write_data(page_num, abstract)
            except:
                self.write_data(page_num, "Abstract não encontrado...")

        self.drivers[(page_num - 1)].quit()
