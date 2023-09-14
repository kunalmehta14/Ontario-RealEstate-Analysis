from spiders.spiders.wikicityspider import WikiCitySpider
from spiders.spiders.wikischoolurls import WikiSchoolUrlSpider
from spiders.spiders.zillowspider import ZillowcaSpider
from spiders.spiders.yelpspider import YelpSpider
from spiders.spiders.ongovschoolspider import OnGovSchoolSpider
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy import signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings 
from scrapy.utils.log import configure_logging
import warnings

def main():
  warnings.filterwarnings("ignore")
  wikicity_output = []
  wikischoolurls_output = []
  def crawler_results(item, spider):
    if spider.name == 'wikicity':
      wikicity_output.append(item)
    elif spider.name == 'wikischoolurl':
      wikischoolurls_output.append(item)
  dispatcher.connect(crawler_results, signal=signals.item_scraped)
  #The settings are required to override the default settings used
  #by the spiders.
  settings = get_project_settings()
  configure_logging(settings)
  #To add the city names from the city data collected from Wikipedia
  list_cities = []
  runner = CrawlerRunner(settings)
  @defer.inlineCallbacks
  def crawl():
    yield runner.crawl(WikiCitySpider)
    for item in wikicity_output:
      #This filters the city names appending process as, by default, 
      # the list contains two entries with the name Hamilton. 
      # Zillow only has data for the Hamilton city, not the township.
      if item['cityname'] == 'Hamilton' and item['cityType'] == 'Township':
        pass
      else:
        list_cities.append(item['cityname'])
    yield runner.crawl(WikiSchoolUrlSpider)
    yield runner.crawl(OnGovSchoolSpider, urls=wikischoolurls_output[0]['urls'])
    yield runner.crawl(ZillowcaSpider, cities=list_cities)
    yield runner.crawl(YelpSpider, cities=list_cities)
    reactor.stop()
  crawl()
  reactor.run()
  
if __name__ == '__main__':
  main()