import scrapy, json
from datetime import datetime

class AirbnbSpider(scrapy.Spider):
  name = 'airbnblistings'
  def __init__(self, cities=None, *args, **kwargs):
    super(AirbnbSpider, self).__init__(*args, **kwargs)
    urls = []
    for city in cities:
      city = city.lower().replace(" ", "").replace(",", "").replace(".", "").replace("-", "").replace("/", "").replace("-", "")
      urls.append(f'https://www.airbnb.ca/s/{city}--Canada/homes')
    self.start_urls = urls
  def parse(self, response):
    returned_data = response.selector.xpath('//script[@id="data-deferred-state"]/text()').extract()[0]
    returned_url = response.selector.xpath('//meta[@property="og:url"]/@content').extract()
    updated_data = json.loads(returned_data.replace('\\u00a0', '').replace('\\\\', '').strip())
    results = updated_data['niobeMinimalClientData'][0][1]['data']['presentation']
    stay_search = None
    try:
      stay_search = results['staysSearch']
    except:
      stay_search = results['explore']['sections']['sectionIndependentData']['staysSearch']
    listings = stay_search['results']['searchResults']
    timestamp = datetime.now()
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    for listing in listings:
      yield {
        'id': listing['listing']['id'],
        'name': listing['listing']['name'],
        'listingObjType': listing['listing']['listingObjType'],
        'city': listing['listing']['city'],
        'lat': listing['listing']['coordinate']['latitude'],
        'lon': listing['listing']['coordinate']['longitude'],
        'roomTypeCategory': listing['listing']['roomTypeCategory'],
        'price': listing['pricingQuote']['rate']['amount'],
        'timestamp': timestamp
      }
    next_page = None
    try:
      next_page = stay_search['paginationInfo']['nextPageCursor']
    except:
      pass
    if next_page != None:
      try:
        yield response.follow(f'{returned_url[0]}/homes?cursor={next_page}', callback=self.parse)
      except:
        pass