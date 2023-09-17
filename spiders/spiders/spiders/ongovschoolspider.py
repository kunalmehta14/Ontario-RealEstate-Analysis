import scrapy, re, os
from geopy.geocoders import Bing
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
#Spider to get list of SChool IDs to use for creating URLS to
#fetch school data for Secondary Schools
class OnGovSecSchoolIdSpider(scrapy.Spider):
  name = 'ongovsecschoolid'
  start_urls = ['https://www.app.edu.gov.on.ca/eng/sift/indexSec.asp']
  def parse(self, response):
    data = response.xpath('//select[@id="SCH_NUMBER"]/option/@value').extract() 
    yield {
      'schoolIds': data
    }
#Spider to get list of SChool IDs to use for creating URLS to
#fetch school data for Elementary Schools
class OnGovElSchoolIdSpider(scrapy.Spider):
  name = 'ongovelschoolid'
  start_urls = ['https://www.app.edu.gov.on.ca/eng/sift/index.asp']
  def parse(self, response):
    data = response.xpath('//select[@id="SCH_NUMBER"]/option/@value').extract() 
    yield {
      'schoolIds': data
    }
#This spider uses 'ongovsecschoolid' to get the School Ids
#Get ontario secondary and elementary schools' information from 'app.edu.gov.on.ca'
class OnGovSchoolSpider(scrapy.Spider):
  name = 'ongovschool'
  def __init__(self, elSchoolIds=None, secSchoolIds=None, *args, **kwargs):
    super(OnGovSchoolSpider, self).__init__(*args, **kwargs)
    urls = []
    for schoolId in secSchoolIds:
      urls.append(f'https://www.app.edu.gov.on.ca/eng/sift/schoolProfileSec.asp?SCH_NUMBER={schoolId}')
    for schoolId in elSchoolIds:
      urls.append(f'https://www.app.edu.gov.on.ca/eng/sift/schoolProfile.asp?SCH_NUMBER={schoolId}')
    self.start_urls = urls
  def parse(self, response):
    g = Bing(api_key=os.getenv("BING_MAPS_API"))
    school_address = response.selector.xpath('//div[@class="content"]/div/text()')
    school_name = response.selector.xpath('//h2/text()')
    location = g.geocode(school_address.get())
    school_lat = location.raw['point']['coordinates'][0]
    school_lon = location.raw['point']['coordinates'][1]
    school_city = location.raw['address']['locality']
    yield {
      'schoolid': re.findall('\((\d+)\)', school_name.get())[0],
      'name': re.sub(r'\((\d+)+\)', '', school_name.get()),
      'address': school_address.get(),
      'lat': school_lat,
      'lon': school_lon,
      'city': school_city,
    }
