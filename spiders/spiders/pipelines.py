import mysql
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
    self.store_db(item)
    return item
  def store_db(self, item):
    self.curr.execute(""" insert into """)