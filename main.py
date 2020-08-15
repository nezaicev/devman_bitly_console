import requests
import argparse
import os

from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
URL_GENERATE_BITLINK = 'https://api-ssl.bitly.com/v4/bitlinks'
URL_COUNT_CLICKS = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'


def shorten_link(link, headers):
    bitlink = {'long_url': link}
    response = requests.post(URL_GENERATE_BITLINK, headers=headers, json=bitlink)
    return response.json()


def count_clicks(bitlink, headers):
    params = {'unit': 'day', 'units': -1}
    url = URL_COUNT_CLICKS.format(bitlink)
    response = requests.get(url, headers=headers, params=params)
    return response.json()['total_clicks']


def main():
    parser = argparse.ArgumentParser(
        description="Описание"
    )
    parser.add_argument('link', help='Ссылка на ресурс')
    headers = {'Authorization': 'Bearer {}'.format(TOKEN)}
    link_parse = urlparse(parser.parse_args().link)

    try:
        requests.get(link_parse.geturl()).raise_for_status()
        if link_parse.netloc.startswith('bit.ly'):
            id_bitlink = link_parse.netloc + link_parse.path
            print('По вашей ссылке прошли:', count_clicks(id_bitlink, headers), 'раз(а)')
        else:
            bitlink = shorten_link(link_parse.geturl(), headers)
            print('Короткая ссылка: ', bitlink['link'])
    except requests.exceptions.HTTPError:
        print("Ссылка не существует!")


if __name__ == "__main__":
    main()
