# TODO: drop and remake table md_products
# TODO: merge no_of_pages and price_extract to reduce page requests

import requests
import sqlite3
import time
from bs4 import BeautifulSoup

def count_calls(func):
    # Counter variable
    count = 0

    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        return func(*args, **kwargs)

    def get_call_count():
        return count

    wrapper.get_call_count = get_call_count
    return wrapper

@count_calls
def generate_soup(URL_, return_none=False):
    max_retries = 3
    retry_delay = 5

    if return_none:
        return None

    for retry in range(max_retries):
        try:
            print("Generating soup for page:", URL_)
            resp = requests.get(URL_, timeout=10)
            print(resp.status_code)
            if resp.status_code == 200:
                return BeautifulSoup(resp.text, 'html5lib')
            else:
                print(f"Re-requesting page {URL_} after a {retry_delay}-second delay")
                time.sleep(retry_delay)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if "No scheme supplied" in str(e):
                print("Skipping retry for 'No scheme supplied' error.")
                break
            elif retry < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                break

    return None

def md_all_category_links(homepage_URL):
    soup = generate_soup(homepage_URL)
    clearfix = soup.find_all('a', class_="clearfix")
    return [a['href'] for a in clearfix]

# TODO: It might be possible to skip this step or integrate this with categories to execute these better
def no_of_pages(pagelinks): # number of pages for each category link
    # final dict = {"category": ["link", pages]}
    categories = [link.split(sep="/")[-1] for link in pagelinks]
    page_dict = {}
    for category, link in zip(categories, pagelinks):
        try:
            # print(link)
            page_soup = generate_soup(link)
            no_of_pages = page_soup.find('div', class_="product-filter product-filter-bottom filters-panel")    
            page_dict[category] = [link, int(no_of_pages.text.split(sep="(")[-1].split()[0])]
            print(category)
        except:
            continue
    return page_dict

def product_details_from_list(listings, category):
    titles_prices = []
    for list_item in listings:
        title_and_link = list_item.find('h4')
        print(title_and_link)
        title = title_and_link.text
        link = title_and_link.find('a')['href']
        price = list_item.find('span', class_="price-new").text
        price = int(price[1:].strip().replace(",", ""))
        titles_prices.append((link, category, title, price))
    return titles_prices

def add_to_database_md(triplet, cursor): 
    cursor.execute("INSERT INTO md_products (link, category, title, price, date) VALUES (?, ?, ?, ?, CURRENT_DATE)", triplet)
    print("Added price for product: ", triplet[2], ":", triplet[3])


homepage_MD = "https://mdcomputers.in"
page_number_append = '?page=%%'

links = md_all_category_links(homepage_MD)
page_number_dict = no_of_pages(links)
# print(page_number_dict)

# Not working on these categories here, yet. TODO remove later
del page_number_dict['peripherals']
del page_number_dict['gamerszone']
del page_number_dict['diy-or-custom-cooling']

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
print("Created Database cursor")

# loop 1: create pagewise link from base links from homepage+page limit from no_of_pages function
#   loop 2: create page number soup object for all products by page
#       function to get products from pages
for category, (link, pages) in page_number_dict.items():
    base_link = link+page_number_append
    for page_number in range(1, pages + 1):
        current_link = base_link.replace('%%', str(page_number))
        # print(current_link)
        current_page_soup = generate_soup(current_link, return_none=True)
        try:    
            listings_in_page = current_page_soup.find_all('div', class_="right-block right-b")
            titles_prices = product_details_from_list(listings_in_page, category)
            # print(titles_prices)
            for triplet in titles_prices:
                add_to_database_md(triplet, cursor)
                # so far implemented a "line-item" table that gets you ALL products for ALL days
        except:
            print(f"Invalid page without products")

conn.commit() and conn.close()
print("Total Requests made for one script run:", generate_soup.get_call_count())