import requests
from parsel import Selector

from constants import URL_DOMAIN, HEADERS
from constants import XPATH_PAGINATOR_TOTAL_PAGES, XPATH_ITEM_URLS_IN_CATALOG
from constants import XPATH_ITEM_TITLE, XPATH_ITEM_DESCRIPTION, XPATH_ITEM_PRICE, XPATH_ITEM_ROOMS, XPATH_ITEM_AREA, XPATH_ITEM_PARAMETERS


class Scraper(object):

    def __init__(self, url):
        self.url = url

    def get_html_page(self) -> Selector:
        response = requests.request("GET", self.url, headers=HEADERS)
        return Selector(text=response.text) if response.ok else None

    @staticmethod
    def exctract_paginator_pages_in_catalog(tree: Selector) -> int:
        total_pages_text = tree.xpath(XPATH_PAGINATOR_TOTAL_PAGES).extract_first()
        return int(total_pages_text.split(" ")[3]) if total_pages_text else 0
    
    @staticmethod
    def exctract_apart_urls_in_catalog(tree: Selector) -> list:
        apart_urls = tree.xpath(XPATH_APART_URLS).extract()
        if not apart_urls:
            return []
        return [URL_DOMAIN + apart_url for apart_url in apart_urls]
    
    @staticmethod
    def exctract_apart_data(tree: Selector) -> dict:
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
        
        parameters = tree.xpath(XPATH_ITEM_PARAMETERS)
        parameters = dict(tr.xpath("td/text()").extract() for tr in parameters)
        for key, val in parameters.items():
            if val == "nincs megadva":
                parameters[key] = None
        
        apart_data = dict(
            title=title,
            price=price,
            rooms=rooms,
            area=area,
            **parameters,
            description=description,
        )

        return apart_data