import scrapy, json
from datetime import datetime

class MortgageRatesSpider(scrapy.Spider):
  name = 'mortgagerates'
  start_urls = ['https://www.superbrokers.ca/tools/mortgage-rates-comparison']
  def parse(self, response):
    banks = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    banks = json.loads(banks)
    banks = banks['props']['pageProps']['lenders']
    timestamp = datetime.now()
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    for bank in banks:
      variable = None
      sixmonth = None
      oneyear = None
      twoyear = None
      threeyear = None
      fouryear = None
      fiveyear = None
      for rate in bank['rates']:
        if rate['id'] == 'lovar':
          variable = rate['current']
        elif rate['id'] == 'lcm06':
          sixmonth = rate['current']
        elif rate['id'] == 'lcy01':
          oneyear = rate['current']
        elif rate['id'] == 'lcy02':
          twoyear = rate['current']
        elif rate['id'] == 'lcy03':
          threeyear = rate['current']
        elif rate['id'] == 'lcy04':
          fouryear = rate['current']
        elif rate['id'] == 'lcy05':
          fiveyear = rate['current']
      yield {
        'lender': bank['name'],
        'variable': variable,
        'sixmonth': sixmonth,
        'oneyear': oneyear,
        'twoyear': twoyear,
        'threeyear': threeyear,
        'fouryear': fouryear,
        'fiveyear': fiveyear,
        'timestamp': timestamp
      }