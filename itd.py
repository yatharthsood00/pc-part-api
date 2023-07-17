import requests
from bs4 import BeautifulSoup
# import os
import urllib3
from database_utils import *

urllib3.disable_warnings()

# categories! to get through all products for itdepot. Can add categories here to get more products,
# for now only the most obvious candidates stay here
category_dict = {
    "Cabinets": 5,
    "Cooling": 10,
    "Graphics Cards": 45,
    "HDDs": 12,
    "Memory": 6,
    "Monitors": 7,
    "Motherboards": 13,
    "PSU": 14,
    "Procesors": 30,
    "SSDs": 93,
    "Laptops": 27,
}

# very uncharted territory here:
class Product:
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
    
    # For getting the SQL data string properly, won't change by website
    # solely depends on database_utils.py
    def get_tuple(self):
        #LNPIDC mnemonic "LMP, IDC"
        return (self.link, self.name, self.price, self.instock, self.category)

DatabaseUtil = DatabaseUtils(database_file="database.db", website_name="theitdepot") # TODO: website name can be abstracted
DatabaseUtil.create_table()

# request data "maker", loop for ALL product requests begins here
for category in category_dict:
    data = {
        'filter-limit': '99999',
        'category': str(category_dict[category]),
        'filter': 'true',
    }

    response = requests.post('https://www.theitdepot.com/category_filter.php', data=data, verify=False)

    soup = BeautifulSoup(response.text, 'html5lib')
    # with open(os.path.join(os.getcwd(), 'itd-Cabinets.html'), 'w') as file:
    #     file.write(soup.prettify())

    total_items = soup.find_all("div", class_="product-item col-6 col-md-4 col-lg-3 p-1")

    for item_html in total_items:
        product = Product(item_html, category)
        DatabaseUtil.append_data_to_table(product.get_tuple())

DatabaseUtil.close()
# print(product.html_block.prettify())
