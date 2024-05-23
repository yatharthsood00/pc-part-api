# Meta stuff, for reference
SITES = {'PGB': 'PrimeABGB', 'MDC': 'MD Computers', 'ITD': "TheITDepot"}

# database variables
WEBSITE_TABLES = {
                  "ITD": "itd_products",
                  "MDC": "mdc_products",
                  "PGB": "pgb_products",

                }

DATABASEFILE = 'database.db'

# categories! to get through all products for itdepot. Can add categories here to get more products,
# for now only the most obvious candidates stay here

categories_master_list = [
    "Processor",
    "Cooler",
    "Motherboard",
    "Memory",
    "SSD",
    "HDD",
    "GPU",
    "Case",
    "PSU",
    "Monitor",
]

CATEGORIES = {
    "ITD": {
            "Processor": 30,
            "Cooler": 10,
            "Motherboard": 13,
            "Memory": 6,
            "SSD": 93,
            "HDD": 12,
            "GPU": 45,
            "Case": 5,
            "PSU": 14,
            "Monitor": 7,
        },
    "PGB": {
            "Processor": "cpu-processor",
            "Cooler": "cpu-cooler",
            "Motherboard": "motherboards",
            "Memory": "ram-memory",
            "SSD": "ssd",
            "HDD": "internal-hard-drive",
            "GPU": "graphic-cards-gpu",
            "Case": "pc-cases-cabinet",
            "PSU": "power-supplies-smps",
            "Monitor": "led-monitors",
        },
    "MDC": {
            "Processor": "processor",
            "Cooler": "cooling-system",
            "Motherboard": "motherboards",
            "Memory": "memory",
            "SSD": "ssd-drive",
            "HDD": "internal-hdd",
            "GPU": "graphics-card",
            "Case": "cabinet",
            "PSU": "smps",
            "Monitor": "monitors",
    }
}

itd_categories = {
    "Processor": 30,
    "Cooler": 10,
    "Motherboard": 13,
    "Memory": 6,
    "SSD": 93,
    "HDD": 12,
    "GPU": 45,
    "Case": 5,
    "PSU": 14,
    "Monitor": 7,

}

pgb_categories = {
    "Processor": "cpu-processor",
    "Cooler": "cpu-cooler",
    "Motherboard": "motherboards",
    "Memory": "ram-memory",
    "SSD": "ssd",
    "HDD": "internal-hard-drive",
    "GPU": "graphic-cards-gpu",
    "Case": "pc-cases-cabinet",
    "PSU": "power-supplies-smps",
    "Monitor": "led-monitors",

}

mdc_categories = {
    "Processor": "processor",
    "Cooler": "cooling-system",
    "Motherboard": "motherboards",
    "Memory": "memory",
    "SSD": "ssd-drive",
    "HDD": "internal-hdd",
    "GPU": "graphics-card",
    "Case": "cabinet",
    "PSU": "smps",
    "Monitor": "monitors",
}


# Crawler Variables
SITEPAGES = {
    "PGB": "https://www.primeabgb.com/buy-online-price-india/",
    "ITD": "https://www.theitdepot.com/category_filter.php/",
    "MDC": "https://mdcomputers.in/",

}

SITE_PARAMS = {
    "ITD": {
        'filter-limit': '9999',
        'category': '', #str(itd_category_dict[category])
        'filter': 'true',
    },
    "PGB": {
        'per_page': '9999',
    },
    "MDC": {
        'page': '' # replaced with in-loop page numbers
    },

}

site_product_class = {
    "PGB": "product-wrapper",
    "ITD": "product-item col-6 col-md-4 col-lg-3 p-1",
    "MDC": "right-block right-b"
}

class SitePack:
    '''Full-featured class for all website-specific methods
    starting with URLs and Params
    '''

    def __init__(self, sitename):
        self.site = sitename
        self.categories = CATEGORIES[self.site]
        self.sitepage = SITEPAGES[self.site]

        '''Links:
        output format: dict
        {str -> category: [str -> link-to-the-category, dict -> params]}'''
        if self.site == "PGB":
            self.links_and_params = self.parse_pgb()
        elif self.site == "ITD":
            self.links_and_params = self.parse_itd()
        # elif self.site == "MDC":
        #     self.links = self.parse_mdc()

    def parse_pgb(self):
        '''PGB style: link has category
        Simply append cat_append to base link'''

        urls = {}
        params = SITE_PARAMS["PGB"] # static params for PGB
        for cat, cat_append in self.categories.items():
            link = f"{self.sitepage}{cat_append}"
            urls[cat] = [link, params]
        return urls
    
    def parse_itd(self):
        '''ITD style: link has no category
        param changes for each category'''

        urls = {}
        site_params = SITE_PARAMS["ITD"] # varying param "category", static sitepage
        for cat in self.categories.keys():
            params = site_params.copy()
            params["category"] = str(self.categories[cat])
            # urls.update({cat: [self.sitepage, params]})
            urls[cat] = [self.sitepage, params]

        return urls

        


    