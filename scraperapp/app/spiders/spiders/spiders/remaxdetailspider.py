import scrapy, json, re, os
from datetime import datetime

class RemaxDetailSpider(scrapy.Spider):
  name = 'remaxdetails'
  custom_settings = {
  'FEEDS': {
    'test2.json': {
      'format': 'json'
      }
    }
  }
  start_urls = ['https://www.remax.ca/commercial/on/sioux-lookout-real-estate/lot-4-abram-lake-road-wp_idm73000004-22188598-lst']
#   def __init__(self, listing_urls=None, *args, **kwargs):
#       super(RemaxSpider, self).__init__(*args, **kwargs)
#       urls = []
#       for listing_url in listing_urls:
#         urls.append(listing_url)
#       self.start_urls = urls
  def parse(self, response):
    data = response.selector.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    updated_data = json.loads(data.replace('\\u00a0', '').replace('\\\\', '').strip())
    yield{
      'data': updated_data['props']['pageProps']['dehydratedState']['queries'][0]['state']
    }
