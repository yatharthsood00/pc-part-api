from database_utils import DatabaseUtils
from lister import ProductListing
from crawler import SiteCrawler
from config import *


for site in SITES.values():
    DatabaseUtil = DatabaseUtils(database_file="database.db", website_name=site) 
    DatabaseUtil.create_table()
    print("site: ", site)
    site_html = SiteCrawler(site).blocks
    for htm in site_html:
        product = ProductListing(*htm)
        DatabaseUtil.append_data_to_table(product.get_tuple())
    print("Appended data for table: ", site)
    DatabaseUtil.close()