import re
import requests
from bs4 import BeautifulSoup
import base64
from slugify import slugify


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
            result: dict = {}
            if title := stock_pyload.find('a'):
                result['title'] = title.text
            for detail in stock_pyload.find_all('div', {'class': 'detail'}):
                label = detail.find('span', {'class': 'label'})
                value = detail.find('span', {'class': 'value'})
                result[slugify(label.text)] = value.text
            return result
        except Exception as exception:
            print(stock_pyload)
            print(exception)

    def scraper(self):
        if response := requests.get(self.target):
            pyload = BeautifulSoup(response.text, 'html.parser')
            if stock_table := pyload.find('div', {"class": "active-ipos mt-8"}):
                for stock_frame in stock_table.find_all('div', {'class': 'ipo'}):
                    if result := self.get_item_or_none(stock_frame):
                        self.result.append(result)

    def __len__(self):
        return len(self.__result)

    @property
    def result(self):
        return self.__result


if __name__ == '__main__':
    if scraper := Scraper('https://borsa.doviz.com/halka-arz'):
        print('results ; ')
        print(scraper.result)
