import requests
from bs4 import BeautifulSoup
import urllib3
from database_utils import *
from config import *

urllib3.disable_warnings()

# very uncharted territory here:
# TODO: Making a univ crawler object
# Hands over HTML blocks to ProductListing object
class SiteCrawler:
    def __init__ (self, sitename):
        self.site = self.sitename
        self.page_url = site_pages[site] # function to get siteurl
        self.params = site_params[site]

    def get_pagelist(self):
        resp = requests.post(self.page_url, params=self.params, verify=False)

class ProductListing:
    # TODO: make this a universal class for all websites, starting with PrimeABGB
    def __init__(self, website, html, category):
        # website "TheITDepot"
        if website == "TID":
            self.html_block = html
            self.link = self.get_link_ITD()
            self.name = self.get_product_name_ITD()
            self.price = self.get_price_ITD() 
            self.instock = self.get_stock_status_ITD()
            self.category = category
        
        elif website == "PGB":
            self.html_block = html
            self.link = self.get_link_PGB()
            self.name = self.get_product_name_PGB()
            self.price = self.get_price_PGB() 
            self.instock = self.get_stock_status_PGB()
            self.category = category

        elif website == "MDC":
            self.html_block = html
            self.link = self.get_link_MDC()
            self.name = self.get_product_name_MDC()
            self.price = self.get_price_MDC() 
            self.instock = self.get_stock_status_MDC()
            self.category = category

    # Getting the values functions, change by site
    # TheITDepot
    def get_product_name_ITD(self):
        return self.html_block.find("a", class_="text-dark text-decoration-none")['title']

    def get_price_ITD(self):
        price = self.html_block.find("strong").text.strip()
        return int(price)
    
    def get_stock_status_ITD(self):
        stock_status = 1
        stock_tag = self.html_block.find("span", string="Out of Stock")
        if stock_tag:
            stock_status = 0
        return stock_status

    def get_link_ITD(self):
        sitename = 'https://www.theitdepot.com/'
        product_link = self.html_block.find("a", class_="text-dark text-decoration-none")["href"]
        return sitename+product_link
    
    # PrimeABGB
    def get_product_name_PGB(self):
        return self.html_block.find("h3", class_="product-title").text.strip()

    def get_price_PGB(self):
        price = self.html_block.find('span', class_='price').text
        if price == "Call For Price":
            return -1
        price = price.split(" ")[-1][1:].replace(",","")
        return int(price)
    
    def get_stock_status_PGB(self):
        status = self.html_block.find('span', class_="out-of-stock")
        if status:
            return 0
        else:
            return 1

    def get_link_PGB(self):
        return self.html_block.find('a', class_="woocommerce-LoopProduct-link")['href']

    # MDComputers
    def get_product_name_MDC(self):
        return self.html_block.find('h4').text
    
    def get_link_MDC(self):
        return self.html_block.find('a')['href']

    def get_stock_status_MDC(self):
        # 1 always if its here, if its not on the site its OOS
        return 1

    def get_price_MDC(self):
        price_str = self.html_block.find('span', class_="price-new").text.strip()
        price = price_str[1:].replace(",", "")
        return price
    

    # For getting the SQL data string properly, won't change by website
    # solely depends on database_utils.py
    def get_tuple(self):
        #LNPIDC mnemonic "LMP, I(Date)C"
        return (self.link, self.name, self.price, self.instock, self.category)

DatabaseUtil = DatabaseUtils(database_file="database.db", website_name="theitdepot") 
# TODO: website name can be abstracted
DatabaseUtil.create_table()
website = "TID"

# ITD: request data "maker", loop for ALL product requests begins here

# primary driver code 
# Just a loop for now? Daily execution or something?
# Can later have a cloud scheduler thing and pub/sub system to choose sites

for site in sitenames.values():
    SiteCrawler(site)

for category in itd_category_dict:
    params = {
        'filter-limit': '99999',
        'category': str(itd_category_dict[category]),
        'filter': 'true',
    }

    response = requests.post('https://www.theitdepot.com/category_filter.php', params=params, verify=False)

    soup = BeautifulSoup(response.text, 'html5lib')

    total_items = soup.find_all("div", class_="product-item col-6 col-md-4 col-lg-3 p-1")

    for item_html in total_items:
        product = ProductListing(website, item_html, category)
        DatabaseUtil.append_data_to_table(product.get_tuple())

DatabaseUtil.close()
