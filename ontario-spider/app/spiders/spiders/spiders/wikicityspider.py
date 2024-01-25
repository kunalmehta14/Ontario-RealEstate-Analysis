import scrapy

class WikiCitySpider(scrapy.Spider):
  name = 'wikicity'
  start_urls = ['https://en.wikipedia.org/wiki/List_of_municipalities_in_Ontario']
  def parse(self, response):
    data = response.xpath('//table[contains(@class, "wikitable")]/tbody/tr')
    for item in data:
      if item.xpath('./td/a/text()').extract_first() != None:
        yield {
          'cityname': item.xpath('./th[1]/a/text()').extract()[0],
          'cityType': item.xpath('./td[2]/text()').extract()[0].replace("\n",""),
          'division': item.xpath('./td[3]/a/text()').extract()[0],
          'populationLatest': item.xpath('./td[4]/text()').extract()[0].replace("\n","").replace(",",""),
          'populationPrevious': item.xpath('./td[5]/text()').extract()[0].replace("\n","").replace(",",""),
          'area': item.xpath('./td[7]/span/text()').extract()[0].replace("\n","").replace(",",""),
        }