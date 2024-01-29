import scrapy
import json, time, os
from datetime import datetime
from geopy.geocoders import Bing
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class ZillowcaSpider(scrapy.Spider):
  name = 'zillowca'
  def __init__(self, cities=None, *args, **kwargs):
    super(ZillowcaSpider, self).__init__(*args, **kwargs)
    urls = []
    for city in cities:
      city = city.lower().replace(" ","-").replace("/","-").replace("'","-").replace(".","-").replace("–","-").replace("--","-")
      city = f'{city}-ab'
      urls.append(f'https://www.zillow.com/{city}/')
      urls.append(f'https://www.zillow.com/{city}/sold/')
      urls.append(f'https://www.zillow.com/{city}/rentals/')
    self.start_urls = urls
  def parse(self, response):
    data = response.selector.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    data = json.loads(data)
    results = data['props']['pageProps']['searchPageState']['cat1']
    listings = results['searchResults']['listResults']
    timestamp = datetime.now().date()
    timestamp = timestamp.strftime('%Y-%m-%d')
    for listing in listings:
      #Combines the address attributes to create a single address string
      address = f"{listing['addressStreet']}, {listing['addressCity']}, {listing['addressState']}, {listing['addressZipcode']}"
      #Some listings don't have any beds and baths key
      #Update those key with a custom entry for consistency
      listing_beds = None
      listing_baths = None
      listing_lat = None
      listing_lon = None
      #Checks if listsings has bedrooms
      if 'beds'in listing:
        listing_beds = listing['beds']
      #Checks if listsings has bathrooms
      if 'baths' in listing:
        listing_baths = listing['baths']
      #Some listings don't have the coordinates defined
      #to make sure each listing data is recorded with 
      #location coordinates, use Bing maps API to 
      #get the coordinates using the listing address
      g = Bing(api_key=os.getenv("BING_MAPS_API"))
      address = listing['address']
      if 'latLong' in listing:
        if 'latitude' in listing['latLong'] and 'longitude' in listing['latLong']:
          listing_lat = listing['latLong']['latitude']
          listing_lon = listing['latLong']['longitude']
        else:
          location = g.geocode(address)
          listing_lat = location.raw['point']['coordinates'][0]
          listing_lon = location.raw['point']['coordinates'][1]
      else:
        location = g.geocode(address)
        listing_lat = location.raw['point']['coordinates'][0]
        listing_lon = location.raw['point']['coordinates'][1]
      #Only returns the listings that are in Ontario
      if listing['addressState'] == "AB":
        yield {
          'id': listing['id'],
          'address': listing['address'],
          'addressStreet': listing['addressStreet'],
          'city': listing['addressCity'],
          'beds': listing_beds,
          'baths': listing_baths,
          'price': listing['unformattedPrice'],
          'lat': listing_lat,
          'lon': listing_lon,
          'listingType': listing['hdpData']['homeInfo']['homeType'],
          'saleStatus': listing['hdpData']['homeInfo']['homeStatus'],
          'listingUrl': listing['detailUrl'],
          'timestamp': timestamp
        }
    
    if results != None and 'pagination' in results['searchList']:
      if results['searchList']['pagination'] != None:
        next_page = results['searchList']['pagination']['nextUrl']
        yield response.follow(f'https://www.zillow.com{next_page}', callback=self.parse)
    else:
      pass