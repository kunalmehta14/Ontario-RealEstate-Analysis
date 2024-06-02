import mysql.connector
import os
import datetime
from dotenv import find_dotenv, load_dotenv
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class DownloadListingImages(ImagesPipeline):
  def get_media_requests(self, item, info):
    for image_url in item['images']:
      yield scrapy.Request(image_url, meta={'id': item['id'], 'website': item['website'], 'province': item['province']})
  
  def file_path(self, request, response=None, info=None, *, item=None):
    item_id = request.meta['id']
    website = request.meta['website']
    province = request.meta['province']
    image_name = request.url.split('/')[-1]
    folder_path = f'./{website}/{province}/{item_id}'
    return f'{folder_path}/{image_name}'

insertdate = datetime.date.today()
class MysqlPipeline(object):
  def __init__(self):
    self.create_connection()

  def create_connection(self):
    self.connection = mysql.connector.connect(
      host = os.getenv("MYSQL_HOST"),
      user = os.getenv("MYSQL_USER"),
      password = os.getenv("MYSQL_PASSWORD"),
      database = os.getenv("MYSQL_DATABASE"),
      port = os.getenv("MYSQL_PORT"),
      auth_plugin='mysql_native_password'
    )
    self.cursor = self.connection.cursor()

  def process_item(self, item, spider):
    if spider.name == 'wikicity':
      self.cities_db(item)
    elif spider.name == 'zillowca':
      self.zillow_db(item)
    elif spider.name == 'remaxca':
      self.remax_db(item)
    elif spider.name == 'remaxcameta':
      self.remax_detail_db(item)
    elif spider.name == 'airbnblistings':
      self.airbnb_db(item)
    elif spider.name == 'yelpapi':
      self.yelp_db(item)
    elif spider.name == 'walkscorezillow':
      self.walkscore_zillow_db(item)
    elif spider.name == 'walkscoreremax':
      self.walkscore_remax_db(item)
    return item
  def cities_db(self, item):
    self.cursor.execute(""" insert ignore into CitiesData (CityName, CityType, Division, 
                        PopulationLatest, PopulationPrevious, Area) values (%s, %s, %s, %s, %s, %s)""",(
                        item["cityname"], item["cityType"], item["division"],
                        item["populationLatest"], item["populationPrevious"], item["area"]
                      ))
    self.connection.commit()
  def zillow_db(self, item):
    self.cursor.execute(""" insert ignore into ZillowListings (Id, Address, AddressStreet, CityName, Beds, Baths, 
                        ListingCoordinates, ListingType, ListingUrl) 
                        values (%s, %s, %s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)'), %s, %s)""",(
                        item["id"], item["address"], item["addressStreet"], 
                        item["city"],item["beds"], item["baths"], 
                        item["lat"], item["lon"], 
                        item["listingType"], item['listingUrl']
                      ))
    self.cursor.execute(""" SET FOREIGN_KEY_CHECKS=0 """)
    self.cursor.execute(""" insert ignore into ZillowListingsAssociations (Id, Price, SaleStatus, timestamp) 
                        values (%s, %s, %s, %s)""",(
                        item["id"], item["price"], item["saleStatus"], f'{insertdate}'
                      ))
    self.cursor.execute(""" SET FOREIGN_KEY_CHECKS=1 """)
    self.connection.commit()
  def remax_db(self, item):
    self.cursor.execute(""" insert ignore into RemaxListings (Id, AddressStreet, CityName, Beds, Baths, 
                        ListingCoordinates, ListingType, ListingDate, Area, ListingUrl) 
                        values (%s, %s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)'), %s, %s, %s, %s)""",(
                      item["id"], item["address"], item["city"],item["beds"], item["baths"], 
                      item["lat"], item["lon"], item["listingType"], item['listingDate'], 
                      item['sqft'], item['listingUrl']
                      ))
    self.cursor.execute(""" SET FOREIGN_KEY_CHECKS=0 """)
    self.cursor.execute(""" insert ignore into RemaxListingsAssociations (Id, Price, SaleStatus, timestamp) 
                        values (%s, %s, %s, %s)""",(
                        item["id"], item["price"], item["saleStatus"], f'{insertdate}'
                      ))
    self.cursor.execute(""" SET FOREIGN_KEY_CHECKS=1 """)
    self.connection.commit()
  def remax_detail_db(self, item):
    self.cursor.execute(""" insert ignore into RemaxListingsDetailed (Id, Mls, AgentID, AgentName, AgentOffice,
                        AgentEmail, AgentPhone, Basement, TaxAmount, Fireplace, Garage,
                        Heating, Sewer, SubDivision, Description, Images) 
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE Mls=%s """, (
                        item['id'], item['mlsNum'], item['agentIId'], item['agentName'], item['agentOffice'],
                        item['agentEmail'], item['agentPhone'], item['basement'], item['taxAmount'],
                        item['fireplace'], item['garage'], item['heating'], item['sewer'],
                        item['subDivision'], item['description'], item['image_rest_endpoints'], item['mlsNum']
                        ))
    self.connection.commit()
  def airbnb_db(self, item):
    self.cursor.execute("""  insert ignore into AirbnbData (Id, ListingName, ListingObjType, CityName, 
                        ListingCoordinates, RoomTypeCategory)  
                        values (%s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)'), %s)""",(
                        item["id"], item["name"], item["listingObjType"], item["city"],
                        item["lat"], item["lon"], item["roomTypeCategory"]
                      ))
    self.cursor.execute(""" SET FOREIGN_KEY_CHECKS=0 """)
    self.cursor.execute(""" INSERT IGNORE INTO AirbnbDataAssociations (Id, Price, timestamp) values (%s, %s, %s) """,(
                        item["id"], item["price"], f'{insertdate}'
                      ))
    self.cursor.execute(""" SET FOREIGN_KEY_CHECKS=1 """)
    self.connection.commit()
  def yelp_db(self, item):
    self.cursor.execute(""" insert ignore into YelpData (Id, BusinessName, Rating, Reviews, BusinessAddress, 
                        CityName, BusinessCoordinates) 
                        values (%s, %s, %s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)'))""",(
                        item["id"], item["bizName"],item["rating"], item["reviewCount"], 
                        item["address"], item["city"], item["lat"], item["lon"]
                      ))
    self.cursor.execute(""" insert ignore into YelpBusinessData (Id, Categories, PriceRange, BusinessUrl) 
                        values (%s, %s, %s, %s)""",(
                        item["id"], item['categories'], item['price'], item['url']
                      ))
    self.connection.commit()
  def walkscore_zillow_db(self, item):
    self.cursor.execute("""  insert ignore into ZillowListingsWalkscore (Id, WalkScore, TransitScore)  
                        values (%s, %s, %s)""",(
                        item["id"], item["walk"], item["transit"]
                      ))
    self.connection.commit()
  def walkscore_remax_db(self, item):
    self.cursor.execute("""  insert ignore into RemaxListingsWalkscore (Id, WalkScore, TransitScore)  
                        values (%s, %s, %s)""",(
                        item["id"], item["walk"], item["transit"]
                      ))
    self.connection.commit()