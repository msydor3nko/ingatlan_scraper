from scraper import Scraper


if __name__ == "__main__":
    default_url = "https://ingatlan.com/szukites/kiado+lakas+budapest+havi-60-80-ezer-Ft"
    url = input("Paste the search url: ") or default_url

    # arg: save_to="db" -> need to resolve:
    # "TypeError: __init__() got an unexpected keyword argument 'save_to'"
    scraper = Scraper(url=url)
    scraper.run()

