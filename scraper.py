import re
import csv
import json
from time import sleep

import requests
from parsel import Selector
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from constants import URL_INGATLAN_DOMAIN, HEADERS, RE_APART_PRICE_DIGITS
from constants import XPATH_PAGINATOR_TOTAL_PAGES, XPATH_ITEM_URLS_IN_CATALOG
from constants import XPATH_APART_ADDRESS, XPATH_APART_PRICE, XPATH_APART_ROOMS
from constants import XPATH_APART_AREA, XPATH_APART_DESCRIPTION
from constants import XPATH_APART_PARAMETERS_TABLE, XPATH_APART_PARAMETERS_TROWS
from models import Apartment
from config import DATABASE_CONNECTION


class ScraperBase(object):
    def __init__(self):
        self._engine = create_engine(DATABASE_CONNECTION, echo=True)
        self._session = sessionmaker(bind=self._engine)()
        Apartment.metadata.create_all(self._engine)
        self._is_csv_with_header = False

    def save_data(self, apart_data):
        if self.save_to == "csv":
            self._save_to_csv(apart_data)

        if self.save_to == "db":
            self._save_to_db(apart_data)

    def _save_to_csv(self, apart_data: dict):
        try:
            with open("apart_data.csv", 'a') as csv_file:
                writer = csv.DictWriter(csv_file,
                                        fieldnames=apart_data.keys())
                if not self._is_csv_with_header:
                    writer.writeheader()
                    self._is_csv_with_header = True
                writer.writerow(apart_data)
                print("=== Apart data ===", "\n", apart_data)
        except IOError:
            print("IOError: saving data into CSV")

    def _save_to_db(self, apart_data):
        try:
            apart = Apartment(
                id=apart_data.get('apart_id'),
                url=apart_data.get('url'),
                data_artefacts=apart_data.get('data_artefacts'),
                address=apart_data.get('address'),
                price=apart_data.get('price'),
                rooms=apart_data.get('rooms'),
                area=apart_data.get('area'),
                parameters=apart_data.get('parameters'),
                description=apart_data.get('description'),
            )
            self._session.add(apart)
            self._session.commit()
            print(f'Saved: {apart_data}')

        except Exception as exc:
            print(f"ScraperBase exception: {exc}")

        finally:
            self._session.close()
            print('ScraperBase session closed.')


class Scraper(ScraperBase):

    def __init__(self, url: str, save_to: str):
        super().__init__()
        self._page_count = 0
        self.url = url
        self.save_to = save_to

    def run(self):
        if not (first_catalog_page := self.get_html_response(self.url)):
            return "Bad init request!"

        self.scrape_aparts_on_catalog_page(first_catalog_page)

        self._page_count = self.extract_paginator_on_catalog_page(first_catalog_page) or 1
        if self._page_count > 1:
            self.generate_catalog_page()
        return

    def generate_catalog_page(self):
        catalog_urls = (f"{self.url}?page={n}" for n in range(2, self._page_count + 1))
        for url in catalog_urls:
            print("\nCatalog page generated:", url)
            catalog_page = self.get_html_response(url)
            self.scrape_aparts_on_catalog_page(catalog_page)

    def get_html_response(self, url: str) -> Selector:
        response = requests.request("GET", url, headers=HEADERS)
        return Selector(response.text) if response.ok else None

    def scrape_aparts_on_catalog_page(self, catalog_page: Selector):
        item_urls = self.extract_item_urls_in_catalog(catalog_page)
        for url in item_urls:
            page_tree = self.get_html_response(url)
            apart_data = self.extract_apart_data(page_tree, url)
            self.save_data(apart_data)
            sleep(1)

    def extract_apart_data(self, tree: Selector, apart_url: str) -> dict:
        data_artefacts = {}

        price = self.extract_apart_price(tree)
        if not price["is_done"]:
            data_artefacts.update(price=price["result"])
            price = None
        else:
            price = price["result"]

        rooms = self.extract_apart_rooms(tree)
        if not rooms["is_done"]:
            data_artefacts.update(rooms=rooms["result"])
            rooms = None
        else:
            rooms = rooms["result"]
        
        area = self.extract_apart_area(tree)
        if not area["is_done"]:
            data_artefacts.update(area=area["result"])
            area = None
        else:
            area = area["result"]

        data_artefacts = \
            json.dumps(data_artefacts, ensure_ascii=False) if data_artefacts else None

        apart_id = self.extract_apart_id_from_item_url(apart_url)
        address = self.extract_apart_address(tree)
        description = self.extract_apart_description(tree)
        parameters = self.extract_apart_parameters(tree)

        apart_data = dict(
            apart_id=apart_id,
            url=apart_url,
            data_artefacts=data_artefacts,
            address=address,
            price=price,
            rooms=rooms,
            area=area,
            parameters=parameters,
            description=description,
        )

        return apart_data

    @staticmethod
    def extract_paginator_on_catalog_page(tree: Selector) -> int:
        total_pages_text = tree.xpath(XPATH_PAGINATOR_TOTAL_PAGES).extract_first()
        return int(total_pages_text.split(" ")[3]) if total_pages_text else 0

    @staticmethod
    def extract_item_urls_in_catalog(tree: Selector) -> list:
        apart_urls = tree.xpath(XPATH_ITEM_URLS_IN_CATALOG).extract()
        if not apart_urls:
            return []
        return [URL_INGATLAN_DOMAIN + apart_url for apart_url in apart_urls]

    @staticmethod
    def extract_apart_id_from_item_url(url: str) -> int:
        return int(url.split("/")[-1])

    @staticmethod
    def extract_apart_address(tree: Selector) -> str:
        return tree.xpath(XPATH_APART_ADDRESS).extract_first()

    @staticmethod
    def extract_apart_price(tree: Selector) -> dict:
        price = tree.xpath(XPATH_APART_PRICE).extract_first()
        try:
            price = "".join(RE_APART_PRICE_DIGITS.findall(price))
            return {"result": int(price), "is_done": True}
        except (TypeError, ValueError) as exc:
            print(exc)
            return {"result": price, "is_done": False}

    @staticmethod
    def extract_apart_rooms(tree: Selector) -> dict:
        rooms = tree.xpath(XPATH_APART_ROOMS).extract_first()
        try:
            rooms = int(rooms.strip()) if rooms else None
            return {"result": rooms, "is_done": True}
        except ValueError as exc:
            print(exc)
            return {"result": rooms, "is_done": False}

    @staticmethod
    def extract_apart_area(tree: Selector) -> dict:
        area = tree.xpath(XPATH_APART_AREA).extract_first()
        try:
            area = int(area.strip(" m²")) if area else None
            return {"result": area, "is_done": True}
        except ValueError as exc:
            print(exc)
            return {"result": area, "is_done": False}

    @staticmethod
    def extract_apart_description(tree: Selector) -> str:
        description = tree.xpath(XPATH_APART_DESCRIPTION).extract()
        return " ".join(s.strip() for s in description if s) if description else None

    @staticmethod
    def extract_apart_parameters(tree: Selector) -> str:
        params = tree.xpath(XPATH_APART_PARAMETERS_TABLE)
        try:
            params = dict(tr.xpath(XPATH_APART_PARAMETERS_TROWS).extract() for tr in params)
            params = {k.lower(): v for k, v in params.items()}
            for key, val in params.items():
                if val == "nincs megadva":
                    params[key] = "NA"
            return json.dumps(params, ensure_ascii=False)
        except Exception as exc:
            print(exc)
            return params
