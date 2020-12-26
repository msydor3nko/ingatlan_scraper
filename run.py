from scraper import Scraper


def run(storage="csv"):
    default_url = "https://ingatlan.com/szukites/kiado+lakas+budapest+havi-60-80-ezer-Ft"
    url = input("Paste the search url: ") or default_url
    scraper = Scraper(url=url, save_to=storage)
    scraper.run()


if __name__ == "__main__":
    run()


