# TODO: If any product isn't found in search, it means its OOS. Add a "date added" tag for now to detect this

import requests
from bs4 import BeautifulSoup

def generate_soup(URL_):
    return BeautifulSoup(requests.get(URL_).text, 'html5lib')

def md_all_category_links(homepage_URL):
    soup = generate_soup(homepage_URL)
    clearfix = soup.find_all('a', class_="clearfix")
    return [a['href'] for a in clearfix]

def no_of_pages(pagelinks): # number of pages for each category link
    # final dict = {"category": ["link", pages]}
    categories = [link.split(sep="/")[-1] for link in pagelinks]
    page_dict = {}
    for category, link in zip(categories, pagelinks):
        try:
            print(link)
            page_soup = generate_soup(link)
            no_of_pages = page_soup.find('div', class_="product-filter product-filter-bottom filters-panel")    
            page_dict[category] = [link, int(no_of_pages.text.split(sep="(")[-1].split()[0])]
            # print(page_dict)
        except:
            continue
    return page_dict

homepage_MD = "https://mdcomputers.in"
page_number_append = '?page=%%'

links = md_all_category_links(homepage_MD)
page_number_dict = no_of_pages(links)
# print(page_number_dict)

# Not working on these categories here, yet. TODO remove later
del page_number_dict['peripherals']
del page_number_dict['gamerszone']
del page_number_dict['diy-or-custom-cooling']

# loop 1: create pagewise link from base links from homepage+page limit from no_of_pages function
#   loop 2: create page number soup object for all products by page
#       loop 3: extract listing title, link, price from page
# TODO: sort into functions
for category, (link, pages) in page_number_dict.items():
    base_link = link+page_number_append
    for page_number in range(1, pages + 1):
        current_link = base_link.replace('%%', str(page_number))
        # print(current_link) 
        current_page_soup = generate_soup(current_link)
        listings = current_page_soup.find_all('div', class_="right-block right-b")
        for list_item in listings:
            title = list_item.find('h4').text
            price = list_item.find('span', class_="price-new").text
            # TODO Add database stuff
            # print(title, ":", price) 
                