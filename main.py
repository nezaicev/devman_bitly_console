import requests
import argparse
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

URL_GENERATE_BITLINK = 'https://api-ssl.bitly.com/v4/bitlinks'
URL_COUNT_CLICKS = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'


def shorten_link(link, headers):
    body_request = {'long_url': link}
    response = requests.post(URL_GENERATE_BITLINK, headers=headers, json=body_request)
    response.raise_for_status()
    return response.json()


def count_clicks(bitlink, headers):
    params = {'unit': 'day', 'units': -1}
    url = URL_COUNT_CLICKS.format(bitlink)
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def main():

    parser = argparse.ArgumentParser(
        description="Скрипт позволяет генерировать короткие ссылки и и получать информацию о количестве кликов "
    )
    parser.add_argument('link', help='Ссылка на ресурс')
    headers = {'Authorization': 'Bearer {}'.format(BITLY_GENERIC_ACCESS_TOKEN)}
    link_parse = urlparse(parser.parse_args().link)

    try:
        if link_parse.netloc.startswith('bit.ly'):
            id_bitlink = link_parse.netloc + link_parse.path
            print('По вашей ссылке прошли:', count_clicks(id_bitlink, headers), 'раз(а)')
        else:
            bitlink = shorten_link(link_parse.geturl(), headers)
            print('Короткая ссылка: ', bitlink['link'])
    except requests.exceptions.HTTPError:
        print("Ссылка не существует!")


if __name__ == "__main__":
    load_dotenv()
    BITLY_GENERIC_ACCESS_TOKEN = os.getenv('BITLY_GENERIC_ACCESS_TOKEN')
    main()