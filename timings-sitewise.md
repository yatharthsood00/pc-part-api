Timings
synchronous - PGB

func1:
+ getting response from PGB = 4.74s
+ bs4 basic processing = ~2.4s

func2:
+ more parsing (name, price, stockstatus, link) = ~0.09s (negligible)

async-ing for response and basic processing...

async routine:
1. get the HTML response
2. Process the response

FANTASTIC thing, PGB response is 51s -> 13s

## Async branch, adding the async elements to main:

function workflow for reference:

1. parsing function (async) -> generates blocks of product-wrappers (i.e. all data, by product, in a block of markup)

2. get_list_from_block (sync) -> applied on each listing, get big four (name, price, instock (hard to YES for MDC), link)
3. Database stuff (later)

- wrangling main_async.py from try_scratch.py:
- code organising etc
- made a thing for PGB, let's move to other sites
- and make it config-neutral or sth idk what to call it

MDC thing:
- creating a universal function for getting the product HTML (i.e. the crawler whole)
- abstracted the class to find_all with to config (yay)
- made mdc async fully (GPT still, ugh). Time diff is 90+% (240-255s to 20s)
- does use extra requests to get the number of pages. Has to be disparate from actual pagewise runs because async, error prone
- MDC thing NEEDS several helper functions, needs a separate file to be scripted

ITD thing: later
Database adding: final step

- main function call - integrating MDC+PGB stuff
09/04 - to keep this going for reals, let's keep the scripts separate from each other. Everything integrable (database stuff mostly) can be brought in together, but let's save time
- Can later implement more integration/create a template that can work for all kinds of sites (paginated/bypass-paginated)