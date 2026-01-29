import requests
import os
import json
import sys
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('link')
 
    return parser


def is_shorten_link(token, url):
    params = {
        "access_token": token,
        "v": 5.199,
        "key": urlparse(url).path[1:],
        "interval": "day",
        "intervals_count": 1
    }
    response = requests.post("https://api.vk.ru/method/utils.getLinkStats", params=params)
    response.raise_for_status()

    return 'error' not in response.json()


def shorten_link(token, url):
    params = {
        "access_token": token,
        "v": 5.199,
        "url": url
    }
    response = requests.post("https://api.vk.ru/method/utils.getShortLink", params=params)
    response.raise_for_status()

    return response.json()


def count_clicks(token, link):
    params = {
        "access_token": token,
        "v": 5.199,
        "key": link,
        "interval": "month",
        "intervals_count": 1
    }
    response = requests.post("https://api.vk.ru/method/utils.getLinkStats", params=params)
    response.raise_for_status()

    return response.json()


def main():
    parser = create_parser()
    linkspace = parser.parse_args()
    load_dotenv(".env")
    token = os.environ["VK_SERVICE_KEY"]
    url = linkspace.link

    if is_shorten_link(token, url):
        print("Количество откликов: ", count_clicks(token, urlparse(url).path[1:])['response']['stats'][-1]['views'])
    else:
        try:
            print("Короткая ссылка: ", shorten_link(token, url)['response']['short_url'])
        except KeyError:
            print("Ошибка: ", shorten_link(token, url)['error'])


if __name__ == "__main__":

    main()

