import requests
from bs4 import BeautifulSoup
import urllib3
from database_utils import *
from config import *

urllib3.disable_warnings()


# very uncharted territory here:
# TODO: Making a univ crawler object
class SiteCrawler:
    def __init__ (self, sitename):
        self.site = self.sitename
        self.page_url = site_list_pages["theitdepot"]
        self.params = site_params

    def get_pagelist(self):
        pass

class ProductListing:
    # website = "TheITDepot"
    # TODO: make this a universal class for all websites, starting with PrimeABGB
    def __init__(self, html, category):
        self.html_block = html
        self.link = self.get_link()
        self.name = self.get_product_name()
        self.price = self.get_price()
        self.instock = self.get_stock_status()
        self.category = category
    
    # Getting the values functions, change by site
    # TheITDepot
    def get_product_name(self):
        raise NotImplementedError("Subclasses must override get_product_name()")
    
    def get_price(self):
        raise NotImplementedError("Subclasses must override get_price()")
    
    def get_stock_status(self):
        raise NotImplementedError("Subclasses must override get_stock_status()")

    def get_link(self):
        raise NotImplementedError("Subclasses must override get_link()")
    
    # For getting the SQL data string properly, won't change by website
    # solely depends on database_utils.py
    def get_tuple(self):
        #LNPIDC mnemonic "LMP, IDC"
        return (self.link, self.name, self.price, self.instock, self.category)

class ProductListingITD:
    def __init__(self, html, category):
        self.product = ProductListing(html, category)

        # TheITDepot
    def get_product_name(self):
        return self.html_block.find("a", class_="text-dark text-decoration-none")['title']

    def get_price(self):
        price = self.html_block.find("strong").text.strip()
        return int(price)
    
    def get_stock_status(self):
        stock_status = 1
        stock_tag = self.html_block.find("span", string="Out of Stock")
        if stock_tag:
            stock_status = 0
        return stock_status

    def get_link(self):
        sitename = 'https://www.theitdepot.com/'
        product_link = self.html_block.find("a", class_="text-dark text-decoration-none")["href"]
        return sitename+product_link

DatabaseUtil = DatabaseUtils(database_file="database.db", website_name="theitdepot") # TODO: website name can be abstracted
DatabaseUtil.create_table()

# ITD: request data "maker", loop for ALL product requests begins here
for category in category_dict:
    params = {
        'filter-limit': '99999',
        'category': str(category_dict[category]),
        'filter': 'true',
    }

    response = requests.post('https://www.theitdepot.com/category_filter.php', params=params, verify=False)

    soup = BeautifulSoup(response.text, 'html5lib')

    total_items = soup.find_all("div", class_="product-item col-6 col-md-4 col-lg-3 p-1")

    for item_html in total_items:
        product = ProductListing(item_html, category)
        DatabaseUtil.append_data_to_table(product.get_tuple())

DatabaseUtil.close()
