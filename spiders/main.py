from spiders.spiders.wikicityspider import WikiCitySpider
from spiders.spiders.zillowspider import ZillowcaSpider
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy import signals
from twisted.internet import reactor, defer
# from scrapy.utils.project import get_project_settings 
import warnings, time

def main():
  warnings.filterwarnings("ignore")
  results = []
  def crawler_results(item):
        results.append(item)
  dispatcher.connect(crawler_results, signal=signals.item_scraped)
  # settings = get_project_settings()
  # process = CrawlerProcess(settings)
  # process.crawl(WikiCitySpider)
  # process.crawl(ZillowcaSpider, cities=results)
  # process.start()
  runner = CrawlerRunner()
  list_cities = []
  @defer.inlineCallbacks
  def crawl():
    yield runner.crawl(WikiCitySpider)
    for result in results:
      for k, v in result.items():
        if k == 'cityname' and (v == 'Toronto' or v == 'Guelph'):
          list_cities.append(v)
    runner_kwargs = {
    'spidercls': ZillowcaSpider,
    'cities': list_cities,
    }
    yield runner.crawl(runner_kwargs)
    reactor.stop()
  crawl()
  reactor.run()
  return list_cities
if __name__ == '__main__':
  main()