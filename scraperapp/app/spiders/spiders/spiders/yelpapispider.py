import scrapy, os
from urllib.parse import urlencode
import json
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class YelpApiSpider(scrapy.Spider):
  custom_settings = {
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 180,
    'AUTOTHROTTLE_MAX_DELAY': 240
  }
  name = 'yelpapi'
  params = {
            'limit': 40,
            'offset': 0
           }
  headers = {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_1')} 

  def __init__(self, cities=None, *args, **kwargs):
    super(YelpApiSpider, self).__init__(*args, **kwargs)
    urls = []
    for city in cities:
      city = city.replace(" ","-").replace("/","-").replace("'","-").replace(",","-").replace("–","-")
      city = f'{city}-ON'
      urls.append(f'https://api.yelp.com/v3/businesses/search?location={city}')
    self.start_urls = urls

  def start_requests(self):
      for url in self.start_urls:
        yield scrapy.Request(url=url + '&' + urlencode(self.params), headers=self.headers, method="GET", dont_filter=True)
        self.url = url
  def parse(self, response):
      data = response.json()
      businesses = data['businesses']
      for business in businesses:
        yield {
        'id': business['id'],
        'bizName': business['name'],
        'rating': business['rating'],
        'reviewCount': business['review_count'],
        'address': business['location']['address1'],
        'city': business['location']['city'],
        'lon': business['coordinates']['longitude'],
        'lat': business['coordinates']['latitude']
        }
      params = {
              'limit': 40,
              'offset': (self.params['offset'] + 40)
            }
      if response.status != 400 or params['offset'] < 40:
        yield response.follow(url=self.url + '&' + urlencode(params), headers=self.headers, method="GET", dont_filter=True, callback=self.parse)
      elif response.status == 429:
        self.headers = {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_2')} 
      elif response.status != 400 or params['offset'] > 40 or (response.status == 429 and self.headers == {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_2')}):
        params = None
        return None