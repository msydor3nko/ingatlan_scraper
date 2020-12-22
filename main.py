import requests
from parsel import Selector

from scraper import Scraper
from constants import URL_APART_CATALOG
from constants import XPATH_PAGINATOR_TOTAL_PAGES, XPATH_ITEM_URLS_IN_CATALOG
from constants import XPATH_ITEM_TITLE
from constants import HEADERS


def get_page(url: str) -> Selector:
    response = requests.request("GET", url, headers=HEADERS)
    return Selector(text=response.text) if response.ok else None
     

if __name__ == "__main__":
    URL = 'https://ingatlan.com/vii-ker/kiado+lakas/tegla-epitesu-lakas/31927559'

    scraper = Scraper(URL)
    tree = scraper.get_html_page()
    result = scraper.exctract_apart_data(tree)

    print(result)
