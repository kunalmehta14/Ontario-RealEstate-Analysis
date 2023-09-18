import scrapy, os
import json, time
from datetime import datetime
from geopy.geocoders import Bing
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
class YelpSpider(scrapy.Spider):
  name = 'yelp'
  custom_settings = {
    'FEEDS': {
      'test.json': {
        'format': 'json'
      }
    }
  }
  start_urls = ['https://www.yelp.com/search?find_desc=&find_loc=Toronto+ON']
  # def __init__(self, cities=None, *args, **kwargs):
  #   super(YelpSpider, self).__init__(*args, **kwargs)
  #   urls = []
  #   for city in cities:
  #     city = city.replace(" ","+").replace("/","%2F").replace("'","%27").replace(",","%2C")
  #     city = f'{city}+Ontario'
  #     urls.append(f'https://www.yelp.com/search?find_desc=&find_loc={city}')
  #   self.start_urls = urls
  def parse(self, response):
    data = response.selector.xpath('//script[contains(@data-hypernova-key, "__yelpfrontend__")]/text()').extract()[0]
    data = data.replace("<!--","").replace("-->","")
    data = json.loads(data)
    place_data = data['legacyProps']['searchAppProps']['searchPageProps']
    places = place_data['mainContentComponentsListProps']
    place_locations = place_data['rightRailProps']['searchMapProps']['mapState']['markers']
    timestamp = datetime.now()
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    g = Bing(api_key=os.getenv("BING_MAPS_API"))
    for place in places:
      if place['searchResultLayoutType'] == 'iaResult':
        for location in place_locations:
          if 'resourceId' in location and location['resourceId'] == place['bizId']:
            bing_location = g.reverse(f"{location['location']['latitude']}, {location['location']['longitude']}")
            yield {
                'id': place['bizId'],
                'bizName': place['searchResultBusiness']['name'],
                'rating': place['searchResultBusiness']['rating'],
                'reviewCount': place['searchResultBusiness']['reviewCount'],
                'categories': place['searchResultBusiness']['categories'],
                'lat': location['location']['latitude'],
                'lon': location['location']['longitude'],
                'address': bing_location.raw['name'],
                'city': bing_location.raw['address']['locality']
            }
      time.sleep(1)
    next_page = data['legacyProps']['headerProps']['pageMetaTagsProps']['nextPageUrl']
    if next_page != None:
      yield response.follow(next_page, callback=self.parse)
    else:
      pass 