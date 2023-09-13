import scrapy

class WikiSchoolUrlSpider(scrapy.Spider):
  name = 'wikischoolurl'
  start_urls = ['https://en.wikipedia.org/wiki/List_of_secondary_schools_in_Ontario']
  def parse(self, response):
    data = response.xpath('//ol[@class="references"]')
    urls = data.xpath('//cite/a/@href').extract()
    yield {
      'urls' : urls
    }