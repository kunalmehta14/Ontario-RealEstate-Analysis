import scrapy
import json, time
from datetime import datetime

class ZillowcaSpider(scrapy.Spider):
  name = 'zillowca'
  def __init__(self, cities=None, *args, **kwargs):
    super(ZillowcaSpider, self).__init__(*args, **kwargs)
    urls = []
    for city in cities:
      city = city.lower().replace(" ","-").replace("/","-").replace("'","-").replace(".","-").replace("–","-").replace("--","-")
      city = f'{city}-on'
      urls.append(f'https://www.zillow.com/{city}/')
    self.start_urls = urls
  def parse(self, response):
    data = response.selector.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    data = json.loads(data)
    listings = data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']
    timestamp = datetime.now()
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    for listing in listings:
      address = f"{listing['addressStreet']}, {listing['addressCity']}, {listing['addressState']}, {listing['addressZipcode']}"
      try:
        yield {
          'id': listing['id'],
          'address': address,
          'city': listing['addressCity'],
          'beds': listing['beds'],
          'baths': listing['baths'],
          'price': listing['unformattedPrice'],
          'lat': listing['latLong']['latitude'],
          'lon': listing['latLong']['longitude'],
          'listingType': listing['hdpData']['homeInfo']['homeType'],
          'saleStatus': listing['hdpData']['homeInfo']['homeStatus'],
          'timestamp': timestamp
        }
      except:
        yield {
          'id': listing['id'],
          'address': address,
          'city': listing['addressCity'],
          'beds': 0,
          'baths': 0,
          'price': listing['unformattedPrice'],
          'lat': listing['latLong']['latitude'],
          'lon': listing['latLong']['longitude'],
          'listingType': listing['hdpData']['homeInfo']['homeType'],
          'saleStatus': listing['hdpData']['homeInfo']['homeStatus'],
          'timestamp': timestamp
        }
      time.sleep(1)
    if data['props']['pageProps']['searchPageState']['cat1']['searchList'] != None:
      next_page = data['props']['pageProps']['searchPageState']['cat1']['searchList']['pagination']['nextUrl']
      yield response.follow(f'https://www.zillow.com{next_page}', callback=self.parse)
    else:
      pass     