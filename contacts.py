from constants import HEADERS
import requests

url = "https://ingatlan.com/detailspage/api/29530925"

payload="{\"id\":29530925,\"is_favourite\":false,\"is_hidden\":false,\"is_phone_number_visible\":true,\"phone_numbers\":[]}"
headers = {
  'authority': 'ingatlan.com',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  'content-type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)
print(response.text)