# TODO: 404 links (try entry 16 as a test case) return a traceback, cannot consider feature-complete
# Continue stress-testing after 404 issues are addressed
# TODO: Account for call/email for price
# TODO: Follow MD's script and make this a line item database as well

import requests
from bs4 import BeautifulSoup
import sqlite3

def get_all_product_links(cursor):
    cursor.execute("SELECT id, link, title FROM primeabgb_products")
    results = cursor.fetchall()
    return results

def extract_price(soup):
    try:
        price_element = soup.find('li', class_='selling-price')
        price_text = price_element.text.strip()
        price_value = int(price_text[price_text.index("₹") + 1:].replace(",", ""))
        if price_value == 0:
            price_value = -1 # email for price condition
        return price_value
    except:
        return -1

def check_stock_availability(soup):
    in_stock = 1
    oos_element = soup.find('div', class_='stock-availability out-of-stock')
    if oos_element is not None:
        in_stock = 0
    return in_stock

def add_to_database_abgb(price, stock, id, title, cursor):
    cursor.execute("UPDATE primeabgb_products SET current_price = ?,in_stock = ?, price_timestamp = CURRENT_DATE where id = ?", (price, stock, id))
    print(id, "Added price for product: ", title, price, "instock:", stock)


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

all_rows = get_all_product_links(cursor)

for product in all_rows:
    resp = requests.get(product[1])
    soup = BeautifulSoup(resp.text, 'html5lib')

    item_price = extract_price(soup)
    in_stock = check_stock_availability(soup)
    
    add_to_database_abgb(item_price, in_stock, product[0], product[2], cursor)

conn.commit() and conn.close()
