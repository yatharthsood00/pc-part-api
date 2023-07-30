# Meta stuff, for reference
sitenames = [["primeabgb", "pgb"], ["mdcomputers", "mdc"], ["theitdepot", "itd"]]
website_tables = {
                  "theitdepot": "itd_products",
                  "mdcomputers": "md_products",
                  "primeabgb": "prime_products"
                }

                # categories! to get through all products for itdepot. Can add categories here to get more products,
# for now only the most obvious candidates stay here
itd_category_dict = {
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

# Main Variables
site_list_pages = {
    "primeabgb": "https://www.primeabgb.com",
    "theitdepot": "https://www.theitdepot.com/category_filter.php",
    "mdcomputers": "",
}

site_params = {
    "theitdepot": {
        'filter-limit': '99999',
        'category': str(itd_category_dict[""]), #]),
        'filter': 'true',
    }
}

