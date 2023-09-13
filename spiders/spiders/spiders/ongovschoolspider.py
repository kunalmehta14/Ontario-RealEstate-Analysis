import scrapy
import json

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
    school_address = response.selector.xpath('//div[@class="content"]/div/text()')
    school_name = response.selector.xpath('//h2/text()')
    yield {
      'name': school_name.get(),
      'address': school_address.get()
    }