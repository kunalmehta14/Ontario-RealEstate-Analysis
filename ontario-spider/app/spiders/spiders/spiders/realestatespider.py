import scrapy, json, re, os
from datetime import datetime
from geopy.geocoders import Bing
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class RealEstateSpider(scrapy.Spider):
  name = 'realestateca'
  def __init__(self, cities=None, *args, **kwargs):
    super(RealEstateSpider, self).__init__(*args, **kwargs)
    urls = []
    for city in cities:
      city = city.lower().replace(" ","-").replace("/","-").replace("'","-").replace(".","-").replace("–","-").replace("--","-")
      urls.append(f'https://www.remax.ca/on/{city}-real-estate?pageNumber=1')
      urls.append(f'https://www.remax.ca/on/{city}-real-estate?rentalsOnly=true&pageNumber=1')
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
      #RealEstate uses a dictionary to maintain the listing type into a form of
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

class RealEstateMetaSpider(scrapy.Spider):
  name = 'realestatecameta'
  def __init__(self, url_list=None, *args, **kwargs):
    super(RealEstateMetaSpider, self).__init__(*args, **kwargs)
    self.start_urls = url_list
  def parse(self, response):
    data = response.selector.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    updated_data = json.loads(data.replace('\\u00a0', '').replace('\\\\', '').strip())
    updated_data = updated_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']
    # Agent Information
    agent_name = None
    agent_office = None
    agent_email = None
    agent_phone = None
    agent_id = None
    if 'agent' in updated_data:
      if 'firstName' in updated_data['agent'] and 'lastName' in updated_data['agent']:
        agent_first_name = updated_data['agent']['firstName']
        agent_last_name = updated_data['agent']['lastName']
        agent_name = f'{agent_first_name} {agent_last_name}'
      if 'officeName' in updated_data['agent']:
        agent_office = updated_data['agent']['officeName']
      if 'email' in updated_data['agent']:
        agent_email = updated_data['agent']['email']
      if 'telephone' in updated_data['agent']:
        agent_phone = updated_data['agent']['telephone']
      if 'personifyId' in updated_data['agent']:
        agent_id = updated_data['agent']['personifyId']
    # Other Features
    listingId = None
    if 'listingId' in updated_data:
      listingId = updated_data['listingId']
    basement = None
    if 'basement' in updated_data:
      basement = updated_data['basement']
    tax_amount = None
    if 'taxAmount' in updated_data:
      tax_amount = updated_data['taxAmount']
    fireplace = None
    if 'fireplace' in updated_data:
      fireplace = updated_data['fireplace']
    garage = None
    if 'garage' in updated_data:
      garage = updated_data['garage']
    heating = None
    if 'heating' in updated_data:
      heating = updated_data['heating']
    sewer = None
    if 'sewer' in updated_data:
      sewer = updated_data['sewer']
    sub_division = None
    if 'subDivision' in updated_data:
      sub_division = updated_data['subDivision']
    description = None
    if 'description' in updated_data:
      description = updated_data['description']
    mlsnum = None
    if 'mlsNum' in updated_data:
      mlsnum = updated_data['mlsNum']
    # Website and Region settings
    website = 'remaxca'
    province = 'on'
    # Listing Images
    images = []
    image_rest_endpoints = []
    if 'imageUrls' in updated_data:
      images = updated_data['imageUrls']
    if images != []:
      for image_url in images:
        file_name = image_url.split('/')[-1]
        server_endpoint = f'{os.getenv("IMAGE_FILE_SERVER")}/{website}/{province}/{listingId}'
        rest_endpoint = f'{server_endpoint}/{file_name}'
        image_rest_endpoints.append(rest_endpoint)
    serialized_image_rest_endpoints = json.dumps(image_rest_endpoints)
    yield{
      'id': listingId,
      'mlsNum': mlsnum,
      'website': website,
      'province': province,
      'agentIId': agent_id,
      'agentName': agent_name,
      'agentOffice': agent_office,
      'agentEmail': agent_email,
      'agentPhone': agent_phone,
      'basement': basement,
      'taxAmount': tax_amount,
      'fireplace': fireplace,
      'garage': garage,
      'heating': heating,
      'sewer': sewer,
      'subDivision': sub_division,
      'description': description,
      'images': images,
      'image_rest_endpoints': serialized_image_rest_endpoints
    }