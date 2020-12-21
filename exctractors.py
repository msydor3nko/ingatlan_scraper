import requests
from parsel import Selector

from constants import URL_DOMAIN
from constants import XPATH_PAGINATOR_TOTAL_PAGES, XPATH_ITEM_URLS_IN_CATALOG
from constants import XPATH_ITEM_TITLE, XPATH_ITEM_DESCRIPTION, XPATH_ITEM_PRICE, XPATH_ITEM_ROOMS, XPATH_ITEM_AREA, XPATH_ITEM_PARAMETERS


def exctract_paginator_pages_in_catalog(tree: Selector) -> int:
    total_pages_text = tree.xpath(XPATH_PAGINATOR_TOTAL_PAGES).extract_first()
    return int(total_pages_text.split(" ")[3]) if total_pages_text else 0

def exctract_apart_urls_in_catalog(tree: Selector) -> list:
    apart_urls = tree.xpath(XPATH_APART_URLS).extract()
    if not apart_urls:
        return []
    return [URL_DOMAIN + apart_url for apart_url in apart_urls]

def exctract_apart_page_data(tree: Selector) -> dict:
    result = {}
    
    title = tree.xpath(XPATH_ITEM_TITLE).extract_first()
    
    price = tree.xpath(XPATH_ITEM_PRICE).extract_first()
    price = int(price.strip(" Ft").replace(" ", ""))

    rooms = tree.xpath(XPATH_ITEM_ROOMS).extract_first()
    rooms = int(rooms.strip()) if rooms else None
    
    area = tree.xpath(XPATH_ITEM_AREA).extract_first()
    area = int(area.strip(" m²"))

    description = tree.xpath(XPATH_ITEM_DESCRIPTION).extract_first()
    description = description.strip() if description else None
    
    parameters = tree.xpath(XPATH_ITEM_PARAMETERS).extract()
    parameters = dict(zip(parameters[0::2], parameters[1::2]))
    for key, val in parameters.items():
        if val == "nincs megadva":
            parameters[key] = None
    
    result.update(
        title=title,
        price=price,
        rooms=rooms,
        area=area,
        description=description,
        **parameters,
    )

    return result