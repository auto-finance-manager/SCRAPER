import time

from scrapers.stock_scraper import ScraperManager
import schedule

'''
## task 
borsanın aktiaf olduğu gün ve saatlerde aktif veri kazıma görevi
'''

stock_scraper = ScraperManager()
# stock_scraper.work()

for schedule_item in stock_scraper.get_work_times():
    schedule.every().monday.at(schedule_item).do(stock_scraper.work)
    schedule.every().tuesday.at(schedule_item).do(stock_scraper.work)
    schedule.every().wednesday.at(schedule_item).do(stock_scraper.work)
    schedule.every().thursday.at(schedule_item).do(stock_scraper.work)
    schedule.every().friday.at(schedule_item).do(stock_scraper.work)


while True:
    schedule.run_pending()
    time.sleep(1)


