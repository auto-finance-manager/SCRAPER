import time
import pytz
from datetime import datetime
from scrapers.stock_scraper import Scraper
import requests
import config


logger = config.getLogger('stock-scraper-manager')


class ScraperManager:
    def __init__(self):
        self.scraper = self.get_scraper()
        ...

    def work(self):
        self.send_data_to_api(self.data_to_json())

    @staticmethod
    def get_work_times():
        work_times = []
        # product_time_zone = pytz.timezone('Europe/Istanbul')  # BIST
        # product_time = datetime.now(product_time_zone)
        server_time_zone = pytz.timezone('utc')
        # server_time = datetime.now(server_time_zone)
        for hour in range(8, 18 + 1):
            for minute in range(0, 60, 10):
                product_time = datetime(year=2000, day=1, month=1, hour=hour, minute=minute)
                product_time = product_time.astimezone(server_time_zone)
                product_time_hour = product_time.hour
                product_time_minute = product_time.minute
                work_times.append(f"{product_time_hour:02}:{product_time_minute:02}")
        print(work_times)
        return work_times

    @staticmethod
    def send_data_to_api(data):
        api_data_bind_border: int = 50
        counter: int = 0
        for _ in range(0, len(data), api_data_bind_border):
            counter += 1
            response = requests.post(config.SCRAPER_SYNC_URL / 'share/sync/',
                                     json={'sync_list': data[_:_ + api_data_bind_border]})
            if response.status_code == 200:
                time.sleep(1)
                logger.debug(f'Send to data part({counter})')
            else:
                logger.error(f'Error send to data part({counter})')
        # sen end signal

    def data_to_json(self) -> list:
        try:
            converted_list: list = []
            for result in self.scraper.result:
                converted_list.append({
                    "logo": result.get('logo'),
                    "code": result.get('code'),
                    "title": result.get('title'),
                    "graphic": result.get('frame'),
                    "current_price": result.get('current_price'),
                    "last_updated": result.get('last_update')
                })
            logger.info(f'Scraper data converted to json, scraper items count {len(converted_list)}')
            return converted_list

        except Exception as exception:
            print(exception)

    @staticmethod
    def get_scraper() -> Scraper:
        logger.debug(f'scraper called from manager, FINANCE_DATA_SOURCE_URL={config.FINANCE_DATA_SOURCE_URL}')
        return Scraper(config.FINANCE_DATA_SOURCE_URL / 'hisseler')


if __name__ == '__main__':
    scraper: ScraperManager = ScraperManager()
    scraper.get_work_times()
    scraper.work()

