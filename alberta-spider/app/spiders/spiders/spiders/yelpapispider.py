import scrapy, os
from urllib.parse import urlencode
import re, json
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class YelpApiSpider(scrapy.Spider):
  #This is done because Yelp's Fusion API Only allows 500 request per day.
  #This is to slow down the crawler so that it can run without any interruptions
  custom_settings = {
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 180,
    'AUTOTHROTTLE_MAX_DELAY': 240
  }
  name = 'yelpapi'
  headers = {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_1')}
  def __init__(self, cities=None, *args, **kwargs):
    super(YelpApiSpider, self).__init__(*args, **kwargs)
    urls = []
    for city in cities:
      city = city.replace(" ","-").replace("/","-").replace("'","-").replace(",","-").replace("–","-")
      city = f'{city}-AB'
      urls.append(f'https://api.yelp.com/v3/businesses/search?location={city}&limit=40&offset=0')
    self.start_urls = urls

  def start_requests(self):
      for url in self.start_urls:
        yield scrapy.Request(url=url, headers=self.headers, method="GET", dont_filter=True)
        self.url = url
  def parse(self, response):
      data = response.json()
      businesses = data['businesses']
      for business in businesses:
        categories = None
        price = None
        #Check if categories in business data exist
        if 'categories' in business:
          categories = json.dumps(business['categories'])
        #Check if Price Range data in the business data exist
        if 'price' in business:
          price = business['price']
        if business['location']['state'] == "AB":
          yield {
          'id': business['id'],
          'bizName': business['name'],
          'rating': business['rating'],
          'reviewCount': business['review_count'],
          'address': business['location']['address1'],
          'city': business['location']['city'],
          'lon': business['coordinates']['longitude'],
          'lat': business['coordinates']['latitude'],
          'categories': categories,
          'price': price,
          'url': business['url']
          }
      #The next page with Yelp Fusion API format is done by incrementing the offset
      #Regex query which looks for the offset number in the URL
      offset_match = re.search(r'\d+$', response.request.url)
      #Takes the URL and increments by 40
      next_offset_number = int(offset_match.group()) + 40
      #Adds the new offset in the url and uses that as the next page
      next_url = response.request.url.replace(f'offset={offset_match.group()}', '')
      next_url = f'{next_url}offset={next_offset_number}'
      if response.status != 400 and businesses != []:
        yield response.follow(url=next_url, headers=self.headers, method="GET", dont_filter=True, callback=self.parse)
      elif response.status == 429 and self.headers == {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_1')}:
        #If the response recieves Error 429, the request switches the Authorization to second API token
        #This is done because Yelp's Fusion API Only allows 500 request per day.
        self.headers = {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_2')}
        yield response.follow(url=next_url, headers=self.headers, method="GET", dont_filter=True, callback=self.parse)
      elif response.status == 429 and self.headers == {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_2')}:
        #If the response recieves Error 429, the request switches the Authorization to third API token
        #This is done because Yelp's Fusion API Only allows 500 request per day.
        self.headers = {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_3')}
        yield response.follow(url=next_url, headers=self.headers, method="GET", dont_filter=True, callback=self.parse)
      elif response.status == 429 and self.headers == {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_3')}:
        #If the response recieves Error 429, the request switches the Authorization to third API token
        #This is done because Yelp's Fusion API Only allows 500 request per day.
        self.headers = {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_4')}
        yield response.follow(url=next_url, headers=self.headers, method="GET", dont_filter=True, callback=self.parse)
      elif response.status == 429 and self.headers == {'Authorization' : os.getenv('YELP_FUSION_API_BEARER_TOKEN_4')}:
        pass