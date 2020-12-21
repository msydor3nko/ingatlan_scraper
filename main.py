import requests

URL_APART_CATALOG = "https://ingatlan.com/szukites/kiado+lakas+budapest+havi-60-80-ezer-Ft"
headers = {
  'authority': 'ingatlan.com',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

response = requests.request("GET", URL_APART_CATALOG, headers=headers)

print(response.ok)
# print(response.text)
