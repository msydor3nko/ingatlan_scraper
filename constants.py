# URLS
URL_DOMAIN = "https://ingatlan.com"
URL_APART_CATALOG = URL_DOMAIN + "/szukites/kiado+lakas+budapest+havi-60-80-ezer-Ft"

# REQUEST OPTIONS
HEADERS = {
  'authority': 'ingatlan.com',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

# CATALOG PAGE XPATH
XPATH_PAGINATOR_TOTAL_PAGES = '//div[@class="pagination__page-number"]/text()'
XPATH_ITEM_URLS_IN_CATALOG = '//a[@class="listing__link js-listing-active-area"]/@href'

# ITEM PAGE XPATH
XPATH_ITEM_TITLE = '//h1[@class="js-listing-title"]/text()'
XPATH_ITEM_PRICE = '//div[@class="parameter parameter-price"]/span[@class="parameter-value"]/text()'
XPATH_ITEM_ROOMS = '//div[@class="parameter parameter-room"]/span[@class="parameter-value"]/text()'
XPATH_ITEM_AREA = '//div[@class="parameter parameter-area-size"]/span[@class="parameter-value"]/text()'
XPATH_ITEM_DESCRIPTION = '//div[@class="long-description"]/text()'
XPATH_ITEM_PARAMETERS = '//div[@class="paramterers"]//tr'