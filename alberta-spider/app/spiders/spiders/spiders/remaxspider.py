import scrapy, json, re, os
from datetime import datetime
from geopy.geocoders import Bing
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class RemaxSpider(scrapy.Spider):
    name = 'remaxca'
    def __init__(self, cities=None, *args, **kwargs):
      super(RemaxSpider, self).__init__(*args, **kwargs)
      urls = []
      for city in cities:
        city = city.lower().replace(" ","-").replace("/","-").replace("'","-").replace(".","-").replace("–","-").replace("--","-")
        urls.append(f'https://www.remax.ca/ab/{city}-real-estate?pageNumber=1')
        urls.append(f'https://www.remax.ca/ab/{city}-real-estate?rentalsOnly=true&pageNumber=1')
      self.start_urls = urls
    def parse(self, response):
      data = response.selector.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
      updated_data = json.loads(data.replace('\\u00a0', '').replace('\\\\', '').strip())
      listings = updated_data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['results']
      listing_type_ids = updated_data['props']['pageProps']['__namespaces']['common']['propertyType']['id']
      timestamp = datetime.now().date()
      #Convert it into MySQL accepted date object
      timestamp = timestamp.strftime('%Y-%m-%d')
      for listing in listings:
        #Remax uses a dictionary to maintain the listing type into a form of
        #id to string. This for loop goes through the listingid and check what
        #what is the status associated with that listingid.
        listing_type = None
        for type in listing_type_ids:
          try:
            if str(listing['listingTypeId']) == type:
              listing_type = listing_type_ids.get(type)
          except:
            pass
        #Some listings don't have any beds, baths or sqft key
        #Update those key with a custom entry for consistency
        listing_beds = None
        listing_baths = None
        listing_sqft = None
        listing_lat = None
        listing_lon = None
        listing_date = None
        #Checks if listsings has bedrooms
        if 'beds'in listing:
          listing_beds = listing['beds']
        #Checks if listsings has bathrooms
        if 'baths' in listing:
          listing_baths = listing['baths']
        #Checks if listsings has area defined        
        if 'sqFtSearch' in listing:
          listing_sqft = listing['sqFtSearch']
        else:
          pass
        #Some listings don't have the coordinates defined
        #to make sure each listing data is recorded with 
        #location coordinates, use Bing maps API to 
        #get the coordinates using the listing address
        g = Bing(api_key=os.getenv("BING_MAPS_API"))
        address = f"{listing['address']}, {listing['city']}"
        if 'lat' in listing and 'lng' in listing:
          listing_lat = listing['lat']
          listing_lon = listing['lng']
        else:
          location = g.geocode(address)
          listing_lat = location.raw['point']['coordinates'][0]
          listing_lon = location.raw['point']['coordinates'][1]
        #Strip date from the listed date-time
        #Convert it into MySQL accepted date object
        # datetime_obj = datetime.strptime(listing['listingDate'], "%Y-%m-%d")
        # listing_date = datetime_obj.strftime("%Y-%m-%d")
        #Create listing url by mergin the url returned
        #in the collected data and url used in the response
        listing_url = f"https://www.remax.ca/{listing['detailUrl']}"
        yield {
            'id': listing['listingId'],
            'address': listing['address'],
            'city': listing['city'],
            'beds': listing_beds,
            'baths': listing_baths,
            'price': listing['listPrice'],
            'lat': listing_lat,
            'lon': listing_lon,
            'listingType': listing_type,
            'saleStatus': listing['status'],
            'listingDate': listing['listingDate'],
            'sqft': listing_sqft,
            'listingUrl': listing_url,
            'timestamp': timestamp
          }
      if listings != []:
        try:
          page_number_match = re.search(r'\d+$', response.request.url)
          next_page_number = int(page_number_match.group()) + 1
          next_url = response.request.url.replace(f'pageNumber={page_number_match.group()}', '')
          next_url = f'{next_url}pageNumber={next_page_number}'
          yield response.follow(next_url, callback=self.parse)
        except:
          pass
      else:
        pass