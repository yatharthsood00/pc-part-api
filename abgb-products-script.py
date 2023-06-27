import requests
from bs4 import BeautifulSoup
import os
import sqlite3

def get_page_count(URL):
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, 'html5lib')
    page_numbers = soup.find_all('a', class_='page-numbers')
    return int(page_numbers[3].text)

def get_page(URL):
    print("Getting URL:", URL)
    page = requests.get(URL)
    print("Returned:", page.status_code)
    soup = BeautifulSoup(page.text, 'html5lib')
    return soup

def extract_all_links_in_page(soup):
    all_links = soup.find_all('h3')
    links = []
    for h3 in all_links:
        anchor = h3.find_all('a')
        for a in anchor:
            href = a.get('href')
            text = a.text.strip()
            links.append([text, href])
    return links

def add_to_db_table(db, links): # going page by page
    for pairs in links:
        title = pairs[0]
        link = pairs[1]
        db.execute("INSERT INTO primeabgb_products (title, link) VALUES (?, ?)", (title, link))
    db.commit()

db = sqlite3.connect("database.db")
db.execute("DROP TABLE IF EXISTS primeabgb_products;")
db.execute("CREATE TABLE IF NOT EXISTS primeabgb_products (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT(100), link VARCHAR);")
page_no_URL = "https://www.primeabgb.com/page/1/?s&post_type=product&dgwt_wcas=1&per_page=48"
bare_URL = "https://www.primeabgb.com/page/%%/?s&post_type=product&dgwt_wcas=1&per_page=48"

final_page = get_page_count(page_no_URL)

for page in range(1, final_page + 1):
    print("On page", page)
    cur_URL = bare_URL.replace("%%", str(page))
    soup = get_page(cur_URL)
    add_to_db_table(db, extract_all_links_in_page(soup))
    