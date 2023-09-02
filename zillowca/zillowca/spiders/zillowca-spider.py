import scrapy
import json

class ZillowcaSpider(scrapy.Spider):
  name = 'zillowca'
  cities = ['toronto-on', 'waterloo-on', 'guelph-on', 'kitchner-on', 'london-on']
  start_urls = []
  for city in cities:
    start_urls.append(f'https://www.zillow.com/{city}/')
  def parse(self, response):
    data = response.selector.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    data = json.loads(data)
    listings = data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']
    for listing in listings:
      yield {
        'id': listing['id'],
        'addressStreet': listing['addressStreet'],
        'addressCity': listing['addressCity'],
        'addressState': listing['addressState'],
        'addressZipcode': listing['addressZipcode'],
        'beds': listing['beds'],
        'baths': listing['baths'],
        'price': listing['unformattedPrice'],
        'location': listing['latLong'],
        'type': listing['hdpData']['homeInfo']['homeType'],
        'saleStatus': listing['hdpData']['homeInfo']['homeStatus']
      }
    next_page = data['props']['pageProps']['searchPageState']['cat1']['searchList']['pagination']['nextUrl']
    if next_page != None:
      yield response.follow(f'https://www.zillow.com{next_page}', callback=self.parse)
    else:
      pass     