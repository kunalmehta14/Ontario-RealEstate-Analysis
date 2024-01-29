import scrapy

class WikiUrbanCitySpider(scrapy.Spider):
  name = 'wikiurbancity'
  start_urls = ['https://en.wikipedia.org/wiki/List_of_municipalities_in_Alberta']
  def parse(self, response):
    data = response.xpath('//table[contains(@class, "wikitable")][1]/tbody/tr')
    for item in data:
      cityname = item.xpath('./th[contains(@scope, "row")]/a/text()').extract_first()
      if cityname != None:
        yield {
          'cityname': cityname,
          'cityType': item.xpath('./td[1]/text()').extract()[0],
          'populationLatest': item.xpath('./td[3]/text()').extract()[0].replace("\n","").replace(",",""),
          'populationPrevious': item.xpath('./td[4]/text()').extract()[0].replace("\n","").replace(",",""),
          'area': item.xpath('./td[6]/span/text()').extract()[0].replace("\n","").replace(",","")
        }

class WikiRuralCitySpider(scrapy.Spider):
  name = 'wikiruralcity'
  start_urls = ['https://en.wikipedia.org/wiki/List_of_municipalities_in_Alberta']
  def parse(self, response):
    data = response.xpath('//table[contains(@class, "wikitable")][3]/tbody/tr')
    for item in data:
      cityname = item.xpath('./th[contains(@scope, "row")]/a/text()').extract_first()
      if cityname != None:
        yield {
          'cityname': cityname,
          'cityType': item.xpath('./td[1]/a/text()').extract()[0],
          'populationLatest': item.xpath('./td[3]/text()').extract()[0].replace("\n","").replace(",",""),
          'populationPrevious': item.xpath('./td[4]/text()').extract()[0].replace("\n","").replace(",",""),
          'area': item.xpath('./td[6]/span/text()').extract()[0].replace("\n","").replace(",","")
        }

class WikiSpecializedCitySpider(scrapy.Spider):
  name = 'wikispecializedcity'
  start_urls = ['https://en.wikipedia.org/wiki/List_of_municipalities_in_Alberta']
  def parse(self, response):
    data = response.xpath('//table[contains(@class, "wikitable")][2]/tbody/tr')
    for item in data:
      cityname = item.xpath('./th[contains(@scope, "row")]/a/text()').extract_first()
      if cityname != None:
        yield {
          'cityname': cityname,
          'cityType': 'Specialized Municipality',
          'division': item.xpath('./td[1]/a/text()').extract()[0],
          'populationLatest': item.xpath('./td[5]/text()').extract()[0].replace("\n","").replace(",",""),
          'populationPrevious': item.xpath('./td[6]/text()').extract()[0].replace("\n","").replace(",",""),
          'area': item.xpath('./td[8]/span/text()').extract()[0].replace("\n","").replace(",","")
        }