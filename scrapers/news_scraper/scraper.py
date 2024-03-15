import json

import requests
from bs4 import BeautifulSoup
from slugify import slugify

import config


class NewsScraper:
    def work(self):
        if response := requests.get("https://borsa.doviz.com/halka-arz"):
            pyload = BeautifulSoup(response.content, 'html.parser')
            table = pyload.find('div', {"class": 'sidebar'}).find_all('div')
            news: list = []
            for header, value in zip(table[3].find_all('h2'), table[3].find_all('div')):
                news.append({
                    'headline': header.text,
                    'body': str(value)
                })
            return {'news': news}


if __name__ == "__main__":
    scraper = NewsScraper()
    if data := scraper.work():
        requests.post(config.SCRAPER_SYNC_URL / 'share/news/', json=json.dumps(data))

