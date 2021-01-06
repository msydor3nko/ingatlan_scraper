import requests


def translate(text: str):
    content_length = len(text)
    body = {
        'text':text,
        'gfrom':"hu",
        'gto':"en",
        'key':"2989550205ru398"
    }

    headers={
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        # 'content-length': content_length,
        'host': "www.webtran.ru"
    }

    return requests.post(url = 'https://www.webtran.ru/gtranslate/', headers = headers, data=body).text

r = translate(text='nincs megadva')
print(r)


# headers = headers,