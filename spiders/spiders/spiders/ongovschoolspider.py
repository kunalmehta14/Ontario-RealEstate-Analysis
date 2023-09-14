import scrapy
import re
from geopy.geocoders import Nominatim

class OnGovSchoolSpider(scrapy.Spider):
  name = 'ongovschool'
  custom_settings = {
    'FEEDS': {
      'test.json': {
        'format': 'json'
      }
    }
  }
  def __init__(self, urls=None, *args, **kwargs):
    super(OnGovSchoolSpider, self).__init__(*args, **kwargs)
    self.start_urls = urls
  def parse(self, response):
    geolocator = Nominatim(user_agent="ontario_school_data")
    school_address = response.selector.xpath('//div[@class="content"]/div/text()')
    school_name = response.selector.xpath('//h2/text()')
    location = geolocator.geocode(school_address.get())
    school_lat = location.latitude
    school_lon = location.longitude
    yield {
      'schoolid': re.findall('\((\d+)\)', school_name.get())[0],
      'name': re.sub(r'\((\d+)+\)', '', school_name.get()),
      'address': school_address.get(),
      'lat': school_lat,
      'lon': school_lon
    }