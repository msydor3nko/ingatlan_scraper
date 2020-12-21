import requests
from parsel import Selector

import exctractors
from constants import URL_APART_CATALOG
from constants import XPATH_PAGINATOR_TOTAL_PAGES, XPATH_ITEM_URLS_IN_CATALOG
from constants import XPATH_ITEM_TITLE
from constants import HEADERS


def get_page(url: str) -> Selector:
    response = requests.request("GET", url, headers=HEADERS)
    return Selector(text=response.text) if response.ok else None
     

if __name__ == "__main__":
    url = 'https://ingatlan.com/vii-ker/kiado+lakas/tegla-epitesu-lakas/31927559'
    tree = get_page(url)

    # paginator = exctractors.exctract_paginator_pages_in_catalog(tree)
    # aparts_urls = exctractors.exctract_apart_urls_in_catalog(tree)
    result = exctractors.exctract_apart_page_data(tree)

    print(result)