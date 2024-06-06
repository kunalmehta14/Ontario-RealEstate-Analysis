import scrapy
import re

class WalkScoreZillowSpider(scrapy.Spider):
  name = 'walkscorezillow'
  def __init__(self, listings_coordinates=None, *args, **kwargs):
    super(WalkScoreZillowSpider, self).__init__(*args, **kwargs)
    urls = []
    for listing_coordinates in listings_coordinates:
      urls.append(f"https://www.walkscore.com/score/loc/lat={listing_coordinates['lon']}/lng={listing_coordinates['lat']}/id={listing_coordinates['Id']}")
    self.start_urls = urls

  def parse(self, response):
    data = response.xpath('//div[@class="block-header-badge score-info-link"]')
    walkscore = None
    transitscore = None
    for item in data:
      string = item.xpath('./img/@alt').extract()[0]
      #Checks for the score value
      score = re.findall(r'\b\d+\b', string)
      #Checks for the score type in the string
      score_type = re.findall(r'\b\d{2,3}\s+(\w+)', string)
      if score_type[0] == 'Walk':
        walkscore = score[0]
      elif score_type[0] == 'Transit':
        transitscore = score[0]
    # Passing the Zillow and RealEstate listing ID in the WalkScore URL to overcome
    # the limitation to retreive the ID when storing the data in the database
    listing_id = re.search(r'id=(.*)', response.request.url)
    yield {
      'id': listing_id.group(1),
      'walk': walkscore,
      'transit': transitscore
    }

class WalkScoreRealEstateSpider(scrapy.Spider):
  name = 'walkscorerealestate'
  def __init__(self, listings_coordinates=None, *args, **kwargs):
    super(WalkScoreRealEstateSpider, self).__init__(*args, **kwargs)
    urls = []
    for listing_coordinates in listings_coordinates:
      urls.append(f"https://www.walkscore.com/score/loc/lat={listing_coordinates['lon']}/lng={listing_coordinates['lat']}/id={listing_coordinates['Id']}")
    self.start_urls = urls

  def parse(self, response):
    data = response.xpath('//div[@class="block-header-badge score-info-link"]')
    walkscore = None
    transitscore = None
    for item in data:
      string = item.xpath('./img/@alt').extract()[0]
      #Checks for the score value
      score = re.findall(r'\b\d+\b', string)
      #Checks for the score type in the string
      score_type = re.findall(r'\b\d{2,3}\s+(\w+)', string)
      if score_type[0] == 'Walk':
        walkscore = score[0]
      elif score_type[0] == 'Transit':
        transitscore = score[0]
    # Passing the Zillow and RealEstate listing ID in the WalkScore URL to overcome
    # the limitation to retreive the ID when storing the data in the database
    listing_id = re.search(r'id=(.*)', response.request.url)
    yield {
      'id': listing_id.group(1),
      'walk': walkscore,
      'transit': transitscore
    }