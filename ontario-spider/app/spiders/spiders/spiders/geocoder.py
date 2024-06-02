import scrapy
import re

class ZipCodesSpider(scrapy.Spider):
  name = 'zipcodes'
  def __init__(self, cities=None, *args, **kwargs):
    super(ZipCodesSpider, self).__init__(*args, **kwargs)
    urls = []
    for city in cities:
      city = city.lower().replace(" ","+").replace("/","").replace("'","").replace(".","").replace("–","_").replace("--","-")
      urls.append(f'https://www.zip-codes.com/canadian/city.asp?city={city}&province=on')
    self.start_urls = urls

  def parse(self, response):
    list = response.xpath('//ul[contains(@style, "column-count:3")]')
    postal_codes = list.xpath('//li/a[contains(@href, "postalcode")]/text()').extract()
    # Get the name of the city the postal code is associated with
    city = response.xpath('//h1[@class="new"]/text()').extract()[0]
    match = re.match(r'^([^,]+)', city)
    if match:
      city = match.group(1)
    # Loops through the postal codes
    for postal_code in postal_codes:
      yield {
        'city': city,
        'postalcode': postal_code
      }

class GeocoderSpider(scrapy.Spider):
  name = 'geocoder'
  def __init__(self, post_codes=None, *args, **kwargs):
    super(GeocoderSpider, self).__init__(*args, **kwargs)
    urls = []
    for post_code in post_codes:
      post_code = post_code.replace(' ', '')
      urls.append(f'https://geocoder.ca/{post_code}')
    self.start_urls = urls
#   start_urls = ['https://geocoder.ca/M8V1S1']
  def parse(self, response):
    lat = None
    lon = None
    post_code = None
    neighborhood = None
    data = response.xpath('//td[@valign="top"][2]')
    try:
      neighborhood = data.xpath('//p/a/text()').extract()[0]
      neighborhood = neighborhood.replace('Neighborhood of ', '')
    except:
      pass
    try:
      coordinates = data.xpath('//p/strong/text()').extract()[0]
      lat_match = re.match(r'^([^,]+)', coordinates)
      lon_match = re.search(r',\s*(.*)', coordinates)
      if lat_match:
        lat = lat_match.group(1)
      if lon_match:
        lon = lon_match.group(1)
    except:
      pass

    post_code = re.search(r'[^/]+$', response.request.url).group(0)
    post_code = re.sub(r'^(.{3})(.*)$', r'\1 \2', post_code)
    yield {
      'neighborhood': neighborhood,
      'postalcode': post_code,
      'lat': lat,
      'lon': lon
    }