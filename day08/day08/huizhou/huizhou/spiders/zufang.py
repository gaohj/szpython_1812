# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ZufangSpider(CrawlSpider):
    name = 'zufang'
    allowed_domains = ['huizhou.qfang.com']
    start_urls = ['https://huizhou.qfang.com/rent/f1']

    rules = (
        Rule(LinkExtractor(allow=r'https://huizhou.qfang.com/rent/f\d'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('1111')
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
