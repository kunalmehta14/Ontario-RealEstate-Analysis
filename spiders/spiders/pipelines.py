import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# class SpidersPipeline:
#     def process_item(self, item, spider):
#         return item
class MysqlPipeline(object):
  def __init__(self):
    self.create_connection()

  def create_connection(self):
    self.connection = mysql.connector.connect(
      host = os.getenv("MYSQL_HOST"),
      user = os.getenv("MYSQL_USER"),
      password = os.getenv("MYSQL_PASSWORD"),
      database = 'DataAnalysis',
      port = '3306'
    )
    self.curr = self.connection.cursor()
  def process_item(self, item, spider):
    if spider.name == 'wikicity':
      self.cities_db(item)
    elif spider.name == 'zillowca':
      self.zillow_db(item)
    elif spider.name == 'ongovschool':
      self.schools_db(item)
    elif spider.name == 'ongovcol':
      self.colleges_db(item)
    elif spider.name == 'ongovuni':
      self.universities_db(item)
    elif spider.name == 'mortgagerates':
      self.mortgage_db(item)
    return item
  def cities_db(self, item):
    self.curr.execute(""" insert ignore into CitiesData (CityName, CityType, Division, PopulationLatest, PopulationPrevious, Area) values (%s, %s, %s, %s, %s, %s)""",(
                      item["cityname"], item["cityType"], item["division"],
                      item["populationLatest"], item["populationPrevious"], item["area"]
                      ))
    self.connection.commit()
  def zillow_db(self, item):
    self.curr.execute(""" insert ignore into ZillowListings (Id, Address, CityName, Beds, Baths, Price, ListingLat, ListingLon, ListingType, SaleStatus, timestamp) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(
                      item["id"], item["address"], item["city"],item["beds"], item["baths"], 
                      item["price"], item["lat"], item["lon"], item["listingType"],
                      item["saleStatus"], item["timestamp"]
                      ))
    self.connection.commit()
  def schools_db(self, item):
    self.curr.execute(""" insert ignore into SchoolData (Id, SchoolName, SchoolAddress, SchoolLat, SchoolLon, CityName) values (%s, %s, %s, %s, %s, %s)""",(
                      item["schoolId"], item["schoolName"], item["address"],
                      item["lat"], item["lon"], item["city"]
                      ))
    self.connection.commit()
  def colleges_db(self, item):
    self.curr.execute(""" insert ignore into CollegesData (CollegeName, CityName, CollegeAddress, CollegeLat, CollegeLon) values (%s, %s, %s, %s, %s)""",(
                      item["collegeName"], item["city"], item["address"],
                      item["lat"], item["lon"]
                      ))
    self.connection.commit()
  def universities_db(self, item):
    self.curr.execute(""" insert ignore into UniversitiesData (UniversityName, CityName, UniversityAddress, UniversityLat, UniversityLon) values (%s, %s, %s, %s, %s)""",(
                      item["universityName"], item["city"], item["address"],
                      item["lat"], item["lon"]
                      ))
    self.connection.commit()
  def mortgage_db(self, item):
    self.curr.execute(""" insert ignore into MortgageData (LenderName, Variable, SixMonths, OneYear, TwoYears, ThreeYears, FourYears, FiveYears, timestamp) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                      item['lender'], item['variable'], item['sixmonth'],
                      item['oneyear'], item['twoyear'], item['threeyear'],
                      item['fouryear'], item['fiveyear'], item['timestamp']
                      ))