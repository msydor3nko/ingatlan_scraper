from scraper import Scraper
from config import DATA_STORAGE_SETTINGS


def run(storage=DATA_STORAGE_SETTINGS):
    default_url = "https://ingatlan.com/szukites/kiado+lakas+budapest+havi-60-80-ezer-Ft"
    url = input("Paste the search url: ") or default_url
    scraper = Scraper(url=url, save_to=storage)
    scraper.run()


if __name__ == "__main__":
    run()
