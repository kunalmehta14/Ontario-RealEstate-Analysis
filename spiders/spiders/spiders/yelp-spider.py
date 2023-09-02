import scrapy
import json

class YelpSpider(scrapy.Spider):
  name = 'yelp'
  start_urls = ['https://www.yelp.com/search?find_desc=&find_loc=London%2C+Ontario']
  def parse(self, response):
    places_of_interst = []
    data = response.selector.xpath('//script[@data-hypernova-key="yelpfrontend__543172__yelpfrontend__GondolaSearch__dynamic"]/text()').get()
    data = data.replace("<!--","").replace("-->","")
    data = json.loads(data)
    place_data = data['legacyProps']['searchAppProps']['searchPageProps']
    places = place_data['mainContentComponentsListProps']
    place_locations = place_data['rightRailProps']['searchMapProps']['mapState']['markers']
    for place in places:
      if place['searchResultLayoutType'] == 'iaResult':
        for location in place_locations:
          if 'resourceId' in location and location['resourceId'] == place['bizId']:
            yield {
                'id': place['bizId'],
                'bizName': place['searchResultBusiness']['name'],
                'rating': place['searchResultBusiness']['rating'],
                'reviewCount': place['searchResultBusiness']['reviewCount'],
                'categories': place['searchResultBusiness']['categories'],
                'location': location['location']
            }
    next_page = data['legacyProps']['headerProps']['pageMetaTagsProps']['nextPageUrl']
    if next_page != None:
      yield response.follow(next_page, callback=self.parse)
    else:
      pass 