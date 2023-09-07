from spiders.spiders.wikicityspider import WikiCitySpider
from spiders.spiders.zillowspider import ZillowcaSpider
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy import signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings 
from scrapy.utils.log import configure_logging
import warnings, time

def main():
  warnings.filterwarnings("ignore")
  results = []
  def crawler_results(item):
        results.append(item)
  dispatcher.connect(crawler_results, signal=signals.item_scraped)
  settings = get_project_settings()
  # configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
  list_cities = []
  runner = CrawlerRunner(settings)
  @defer.inlineCallbacks
  def crawl():
    yield runner.crawl(WikiCitySpider)
    for result in results:
      if result['cityname'] == 'Hamilton' and result['cityType'] == 'Township':
        pass
      else:
        list_cities.append(result['cityname'])
    yield runner.crawl(ZillowcaSpider, cities=list_cities)
    reactor.stop()
  crawl()
  reactor.run()
  
if __name__ == '__main__':
  main()