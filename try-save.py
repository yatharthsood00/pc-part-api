from bs4 import BeautifulSoup
import os
import webbrowser

# paste below:

import requests

params = {
    'post_type': 'product',
    'per_page': '9999',
    'pa-product-category': 'graphic-cards-gpu',
}

response = requests.get('https://www.primeabgb.com/', params=params)#, cookies=cookies)#, headers=headers)

# driver code, no touchy!

soup = BeautifulSoup(response.text, 'html5lib')

file_path = 'try_list.html'
with open(os.path.join(os.getcwd(), file_path), 'w') as file:
    file.write(soup.prettify())
print("File Created. Opening in browser")

webbrowser.open("file://" + os.path.abspath(file_path))