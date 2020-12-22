import re


# RE PATTERNS
RE_APART_PRICE_DIGITS = re.compile("\d+")

# URLS
URL_INGATLAN_DOMAIN = "https://ingatlan.com"

# REQUEST OPTIONS
HEADERS = {
  'authority': 'ingatlan.com',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

# CATALOG PAGE XPATH
XPATH_PAGINATOR_TOTAL_PAGES = '//div[@class="pagination__page-number"]/text()'
XPATH_ITEM_URLS_IN_CATALOG = '//a[@class="listing__link js-listing-active-area"]/@href'

# ITEM PAGE XPATH
XPATH_APART_ADDRESS = '//h1[@class="js-listing-title"]/text()'
XPATH_APART_PRICE = '//div[@class="parameter parameter-price"]/span[@class="parameter-value"]/text()'
XPATH_APART_ROOMS = '//div[@class="parameter parameter-room"]/span[@class="parameter-value"]/text()'
XPATH_APART_AREA = '//div[@class="parameter parameter-area-size"]/span[@class="parameter-value"]/text()'
XPATH_APART_DESCRIPTION = '//div[@class="long-description"]/text()'
XPATH_APART_PARAMETERS_TABLE = '//div[@class="paramterers"]//tr'
XPATH_APART_PARAMETERS_TROWS = 'td/text()'