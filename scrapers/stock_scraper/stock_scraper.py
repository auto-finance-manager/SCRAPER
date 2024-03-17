import re

import requests
from bs4 import BeautifulSoup
import base64


def get_graphic(source):
    if response := requests.get(source):
        return base64.b64encode(response.content)


class Price:
    """
    CUSTOM INT OBJ FOR DATA SOURCE
    """
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return self.obj

    def __int__(self):
        if type(self.obj) is str:
            return int(self.obj.split(',')[0].replace('.', ''))
        return int(self.obj)

    def __float__(self):
        if type(self.obj) is str:
            pyload = self.obj.split(',')
            if len(pyload) == 1:
                h, d = int(self.obj.split(',')[0].replace('.', '')), 00  # lok af , to .
            elif len(pyload) == 2:
                h, d = int(self.obj.split(',')[0].replace('.', '')), int(self.obj.split(',')[1][:2])
            else:
                raise 'unknown string format'
            return float(f'{h}.{d}')
        return float(self.obj)


def rate(rate_str) -> str:
    pattern = r'([0-9,]+)'
    match = re.search(pattern, rate_str)
    if match:
        return match.group(0)
    return ''


class Scraper(object):
    def __init__(self, target: str):
        self.target = target
        self.__result = []
        self.scraper()

    @staticmethod
    def get_item_or_none(stock_pyload):
        try:
            # print()
            return {
                    'logo':stock_pyload[0].find('img')['src'],
                    'code': stock_pyload[0].find_all('div')[1].text,
                    'title': stock_pyload[0].find_all('div')[2].text,
                    'frame': stock_pyload[7].find('img')['src'],
                    'current_price': float(Price(stock_pyload[1].text)),
                    'rate': stock_pyload[5].text.strip(),
                    'last_update': stock_pyload[6].text.strip(),
                }
        except Exception as exception:
            ... # log

    def scraper(self):
        if response := requests.get(self.target):
            pyload = BeautifulSoup(response.text, 'html.parser')
            stock_table = pyload.find('table', {"id": "stocks"})
            stock_table_body = stock_table.find('tbody')
            for stock_frame in stock_table_body.find_all('tr'):
                if result := self.get_item_or_none(stock_frame.find_all('td')):
                    self.result.append(result)

    def __len__(self):
        return len(self.__result)

    @property
    def result(self):
        return self.__result


if __name__ == '__main__':
    if scraper := Scraper('https://borsa.doviz.com/hisseler'):
        print('results ; ')
        print(scraper.result)
