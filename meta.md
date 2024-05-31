OOS Item Sample: https://mdcomputers.in/fractal-design-era-gold-m-itx-mini-tower.html
In-Stock Sample: https://mdcomputers.in/amd-ryzen-5-7600-100-100001015box.html

Cannot lookup OOS products within website (they get delisted but the page exists so the link is accessible)

Stock/not in stock:
MD: If the product is not seen in the products list as a whole, it is OOS
(basically, query with today's date as WHERE clause gets you all in-stock products @ current prices)
PrimeABGB: Has "Call for Price" or "Email for Price" products. # todo find how to find s/oos from search page direct (reduce page requests)

Crawler:
MD: ITD-like category-filter thing to get all products in one request. Currently way too many requests and parsing needs to be done per script run.
All products that do show up on their website are in-stock. Else all OOS


Sites to be added:
PCStudio - paginated (new function)
VedantComputers - PGB-style
Clarion - paginated (MDC-style, but not using params)

Next steps:
- better organising, run.py script
- Adding next sites and restructuring pagination functions
- Proper logging with logfiles, etc
- Daily scheduled runs (locally for now)