import scrapy, re, os
from geopy.geocoders import Bing
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
#This spider gathers the list of universities in Ontario 
# and the URLs associated with each University.
class OnGovUniListSpider(scrapy.Spider):
  name = 'ongovunilist'
  start_urls = ['https://www.ontariouniversitiesinfo.ca/universities']
  def parse(self, response):
    universities = response.xpath('//article[@class="university"]/h2/a/@href')
    for university in universities:
      yield {
        'university': university.get()
      }
#This spider gets university data
class OnGovUniSpider(scrapy.Spider):
  name = 'ongovuni'
  def __init__(self, university_list=None, *args, **kwargs):
    super(OnGovUniSpider, self).__init__(*args, **kwargs)
    urls = []
    for university in university_list:
      urls.append(f'https://www.ontariouniversitiesinfo.ca{university}')
    self.start_urls = urls
  def parse(self, response):
    uni_name = response.xpath('//h1[@class="template-heading"]/text()').get()
    coordinates = response.xpath('//a[@class="location-directions offsite-noicon"]/@href').get()
    coordinates = coordinates.replace("https://www.google.ca/maps/place/","")
    g = Bing(api_key=os.getenv("BING_MAPS_API"))
    location = g.reverse(coordinates)
    yield {
      'universityName': uni_name,
      'city': location.raw['address']['locality'],
      'address': location.raw['name'],
      'lat': location.raw['point']['coordinates'][0],
      'lon': location.raw['point']['coordinates'][1]
    }
#This spider gathers the list of colleges in Ontario 
# and the URLs associated with each college.
class OnGovColListSpider(scrapy.Spider):
  name = 'ongovcollist'
  start_urls = ['https://www.ontariocolleges.ca/en/colleges']
  def parse(self, response):
    colleges = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"]/a/@href')
    for college in colleges:
      yield {
        'college': college.get()
      }
#This spider gets college data
class OnGovColSpider(scrapy.Spider):
  name = 'ongovcol'
  def __init__(self, college_list=None, *args, **kwargs):
    super(OnGovColSpider, self).__init__(*args, **kwargs)
    urls = []
    for college in college_list:
      urls.append(f'https://www.ontariocolleges.ca{college}')
    self.start_urls = urls
  def parse(self, response):
    campuses = response.xpath('//div[contains(@class, "campus")]')
    college_name = response.xpath('//h1[@id="hero-heading-main"]/text()').extract()[0]
    g = Bing(api_key=os.getenv("BING_MAPS_API"))
    for location in campuses:
      if location.xpath('./span[@class="title"]/text()').extract()[0] != 'Online':
        address_line1 = location.xpath('./span[@class="address"][1]/text()').extract()[0]
        address_line2 = location.xpath('./span[@class="address"][2]/text()').extract()[0]
        location = g.geocode(f'{address_line1}, {address_line2}')
        city = location.raw['address']['locality']
        yield {
          'collegeName': f'{college_name}-{city}',
          'city': city,
          'address': f'{address_line1}, {address_line2}',
          'lat': location.raw['point']['coordinates'][0],
          'lon': location.raw['point']['coordinates'][1]
        }