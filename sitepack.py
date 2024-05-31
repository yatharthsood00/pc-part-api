'''SitePack class definition'''
import requests
from bs4 import BeautifulSoup

from config import (
    CATEGORIES,
    SITEPAGES,
    SITE_PARAMS
)


class SitePack:
    '''Full-featured class for all website-specific methods
    starting with URLs and Params
    '''

    def __init__(self, sitename):
        self.site = sitename
        self.categories = CATEGORIES[self.site]
        self.sitepage = SITEPAGES[self.site]

        '''Links:
        output format: dict
        {str -> category: [str -> link-to-the-category, dict -> params]}
        divclass:
        Class of the div that has the product info (NLPI values)'''

        if self.site == "PGB":
            self.links_and_params = self.parse_pgb()
            self.divclass = 'product-wrapper'
            self.tablename = 'pgb_products'

        elif self.site == "ITD":
            self.links_and_params = self.parse_itd()
            self.divclass = 'product-item col-6 col-md-4 col-lg-3 p-1'
            self.tablename = 'itd_products'

        elif self.site == "MDC":
            self.divclass = 'right-block right-b'
            self.links_and_params = self.parse_mdc()
            self.tablename = 'mdc_products'


    def parse_pgb(self):
        '''PGB style: link has category
        Simply append cat_append to base link'''

        urls = []
        site_params = SITE_PARAMS["PGB"] # static params for PGB
        for cat, cat_append in self.categories.items():
            link = f"{self.sitepage}{cat_append}"
            urls.append([cat, link, site_params])

        return urls

    def parse_itd(self):
        '''ITD style: link has no category
        param changes for each category'''

        urls = []
        site_params = SITE_PARAMS["ITD"] # varying param "category", static sitepage
        for cat in self.categories.keys():
            params = site_params.copy()
            params["category"] = str(self.categories[cat])
            urls.append([cat, self.sitepage, params])

        return urls

    def parse_mdc(self):
        '''MDC style: link has category, but 
        each category is paginated as a param'''

        urls = []
        site_params = SITE_PARAMS["MDC"]
        for cat, cat_append in self.categories.items():
            link = f"{self.sitepage}{cat_append}"
            pagecount = self.mdc_get_pagecount(link)
            print(f"{cat} - {pagecount} pages")
            for i in range(1, pagecount+1):
                params = site_params.copy()
                params["page"] = i
                urls.append((cat, link, params))

        return urls

    def mdc_get_pagecount(self, link):
        '''Unfortunately a synchronous function to get the 
        number of pages in each category'''
        
        resp = requests.get(link, timeout=60)
        soup = BeautifulSoup(resp.text, 'lxml')
        page = soup.find("div", class_="col-sm-6 text-right").text.split(sep=" ")
        return int(page[6][1:])
    
    async def get_pagecount(self, cat, link):
        '''Async process to get the pagecounts for each page in paginated sites'''
        
        pass

    def lister(self, html_block):
        '''Combined function for parsing all params to get
        defined product listing items'''

        name, link, price, stock = "", "", 0, 0

        if self.site == "PGB":
            # 1 - product name
            name = html_block.find("h3", class_="product-title").text.strip()

            # 2 - product link
            link = html_block.find('a', class_="woocommerce-LoopProduct-link")['href']

            # 3 - price
            price = html_block.find('span', class_='price').text
            try:
                price = price.split(" ")[-1][1:].replace(",", "")
                price = int(price)
            except ValueError:
                price = -1

            # 4 - instock indicator
            status = html_block.find('span', class_="out-of-stock")
            if not status:
                stock = 1


        elif self.site == "ITD":
            # 1 - product name
            name = html_block.find("a", class_="text-dark text-decoration-none")['title']

            # 2 - product link
            site = 'https://www.theitdepot.com/'
            link = site + html_block.find("a", class_="text-dark text-decoration-none")["href"]

            # 3 - price
            price = int(html_block.find("strong").text.strip())

            # 4 - instock indicator
            stock_tag = html_block.find("span", string="Out of Stock")
            if not stock_tag:
                stock = 1


        elif self.site == 'MDC':
            # 1 - product name
            name = html_block.find('h4').text

            # 2 - product link
            link = html_block.find('a')['href']

            # 3 - price
            price_str = html_block.find('span', class_="price-new").text.strip()
            price = price_str[1:].replace(",", "")
            price = int(price)

            # 4 - instock indicator
            stock = 1


        return name, link, price, stock