import requests
from parsel import Selector

from scraper import Scraper


if __name__ == "__main__":
    URL = "https://ingatlan.com/szukites/kiado+lakas+budapest+havi-60-80-ezer-Ft"
    
    url = input("Paste the search url: ") or URL

    scraper = Scraper(URL)
    scraper.run()
    
    # tree = scraper.get_html_response(URL)
    # res = tree.xpath(XPATH_ITEM_URLS_IN_CATALOG).extract()
    # print(res)
