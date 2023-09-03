from spiders.spiders.wikicity import WikiCitySpider
from spiders.spiders.yelprestaurants import YelpSpider
from spiders.spiders.zillowca import ZillowcaSpider
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals  
import warnings
def main():
  warnings.filterwarnings("ignore")
  results = []
  def crawler_results(item):
        results.append(item)
  dispatcher.connect(crawler_results, signal=signals.item_scraped)
  process = CrawlerProcess()
  data = process.crawl(WikiCitySpider)
  process.start()
  for result in results:
    for k, v in result.items():
       if k == 'cityname':
        process.crawl(ZillowcaSpider, city=v)

if __name__ == '__main__':
  main()