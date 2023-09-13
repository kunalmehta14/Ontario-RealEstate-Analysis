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
    school_info = response.selector.xpath('//div[@class="content"]/div/text()')
    yield {
        'item': school_info.get()
    }