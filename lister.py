# from bs4 import BeautifulSoup

class ProductListing:

    def __init__(self, website, html, category):

        self.html_block = html
        self.category = category

        if website == "ITD":
            self.name, self.price, self.instock, self.link = self.get_ITD()
        
        elif website == "PGB":
            self.name, self.price, self.instock, self.link = self.get_PGB()

        elif website == "MDC":
            self.name, self.price, self.instock, self.link = self.get_MDC()

    # Getting the values function, change by site

    # TheITDepot    
    def get_ITD(self):
        # 1 - product name
        name = self.html_block.find("a", class_="text-dark text-decoration-none")['title']

        # 2 - price
        price = int(self.html_block.find("strong").text.strip())

        # 3 - instock indicator
        stock = 1
        stock_tag = self.html_block.find("span", string="Out of Stock")
        if stock_tag:
            stock = 0
        
        # 4 - product link
        site = 'https://www.theitdepot.com/'
        link = site + self.html_block.find("a", class_="text-dark text-decoration-none")["href"]

        return name, price, stock, link

    # PrimeABGB
    def get_PGB(self):
        # 1 - product name
        name = self.html_block.find("h3", class_="product-title").text.strip() 

        # 2 - price
        price = self.html_block.find('span', class_='price').text
        try:
            price = price.split(" ")[-1][1:].replace(",", "")
            price = int(price)
        except ValueError:
            price = -1

        # 3 - instock indicator
        status = self.html_block.find('span', class_="out-of-stock")
        if status:
            stock = 0
        else:
            stock = 1

        # 4 - product link
        link = self.html_block.find('a', class_="woocommerce-LoopProduct-link")['href']

        return name, price, stock, link
    

    # MDComputers
    def get_MDC(self):
        # 1 - product name
        name = self.html_block.find('h4').text

        # 2 - price
        price_str = self.html_block.find('span', class_="price-new").text.strip()
        price = price_str[1:].replace(",", "")
        price = int(price) 

        # 3 - instock indicator
        stock = 1 

        # 4 - product link
        link = self.html_block.find('a')['href']

        return name, price, stock, link
    
    # Template to add new sites
    def get_template(self):
        # 1 - product name
        name = self.html_block # parse here

        # 2 - price
        price = int(self.html_block) # parse here

        # 3 - instock indicator
        stock = 1 # logic below

        # 4 - product link
        link = self.html_block # parsing here

        return name, price, stock, link

    # For getting the SQL data string properly, won't change by website
    # solely depends on database_utils.py
    def get_tuple(self):
        #LNPIDC mnemonic "LMP, I(Date)C"
        return (self.link, self.name, self.price, self.instock, self.category)
    
