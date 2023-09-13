# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# class SpidersPipeline:
#     def process_item(self, item, spider):
#         return item

class SpidersPipeline:
  def __init__(self):
    self.items = []
  def process_item(self, item, spider):
    if spider.name == 'special_spider':
      self.items.append(item)
      return item