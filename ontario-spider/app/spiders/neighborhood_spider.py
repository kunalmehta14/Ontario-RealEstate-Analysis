from spiders.spiders.geocoder import ZipCodesSpider, GeocoderSpider
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy import signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import warnings
import os
import mysql.connector
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

def main_remax_meta():
  warnings.filterwarnings("ignore")
  #The settings are required to override the default settings used
  #by the spiders.
  settings = {
    'SCRAPEOPS_API_KEY': os.getenv("SCRAPEOPS_API_KEY"),
    'SCRAPEOPS_FAKE_USER_AGENT_ENABLED': True,
    'DOWNLOADER_MIDDLEWARES': {
      'spiders.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
      'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 401,
      'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 402,
      'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
      'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    },
    'HEADERS': {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate",
      "Connection": "keep-alive",
      "Upgrade-Insecure-Requests": "1",
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "none",
      "Sec-Fetch-User": "?1",
      "Cache-Control": "max-age=0",
    },
    'RETRY_ENABLED': False,
    'RETRY_TIMES': 10,
    'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403],
    'RETRY_PRIORITY_ADJUST': -1,
    'RETRY_EXCEPTIONS': [
      "twisted.internet.defer.TimeoutError",
      "twisted.internet.error.TimeoutError",
      "twisted.internet.error.DNSLookupError",
      "twisted.internet.error.ConnectionRefusedError",
      "twisted.internet.error.ConnectionDone",
      "twisted.internet.error.ConnectError",
      "twisted.internet.error.ConnectionLost",
      "twisted.internet.error.TCPTimedOutError",
      "twisted.web.client.ResponseFailed",
    # OSError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
      OSError,
      "scrapy.core.downloader.handlers.http11.TunnelError",
    ],
    #Logging Settings
    'LOG_FILE': f'/var/log/scrapy.log',
    'LOGGING_ENABLED': True,
    'LOGGING_LEVEL': 'Debug',
    'LOG_STDOUT': True,
    'LOG_FORMAT': "%(levelname)s: %(message)s",
    'ROBOTSTXT_OBEY': False,
    # Set settings whose default value is deprecated to a future-proof value
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': "2.7",
    # TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    'FEED_EXPORT_ENCODING': "utf-8",
    'ITEM_PIPELINES': {
      "spiders.pipelines.MysqlPipeline": 100
    },
    'COOKIES_ENABLED': False,
    'DOWNLOAD_DELAY': 1,
    'DOWNLOAD_FAIL_ON_DATALOSS': False
  }
  configure_logging(settings)
  #MySQL Connection To Query Data for location coordinates
  conn = mysql.connector.connect(
    host = os.getenv("MYSQL_HOST"),
    user = os.getenv("MYSQL_USER"),
    password = os.getenv("MYSQL_PASSWORD"),
    database = os.getenv("MYSQL_DATABASE"),
    port = os.getenv("MYSQL_PORT"),
    auth_plugin='mysql_native_password')
  cursor = conn.cursor(buffered=True , dictionary=True)
  # Get list of cities for the ZipCodesSpider
  cities_data_query = ''' SELECT CitiesData.CityName FROM CitiesData 
                          WHERE NOT EXISTS (SELECT * FROM NeighborhoodData 
                          WHERE NeighborhoodData.CityName = CitiesData.CityName)'''
  cursor.execute(cities_data_query)
  cities_data_result = cursor.fetchall()
  list_cities = []
  for city in cities_data_result:
    list_cities.append(city['CityName'])
  # Get list of post codes for the GeoCoderSpider
  post_code_query = ''' SELECT PostalCode FROM NeighborhoodData
                        WHERE Coordinates IS NULL '''
  cursor.execute(post_code_query)
  post_code_result = cursor.fetchall()
  list_post_codes = []
  for post_code in post_code_result:
    list_post_codes.append(post_code['PostalCode'])
  runner = CrawlerRunner(settings)
  @defer.inlineCallbacks
  def crawl():
    # yield runner.crawl(ZipCodesSpider, cities=list_cities)
    yield runner.crawl(GeocoderSpider, post_codes=list_post_codes)
    reactor.stop()
  crawl()
  reactor.run()

if __name__ == '__main__':
  main_remax_meta()
