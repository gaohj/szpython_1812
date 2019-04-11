# -*- coding: utf-8 -*-
import scrapy
<<<<<<< HEAD
<<<<<<< HEAD
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from bmw.items import BmwItem
class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']
    rules = (
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65.+"),callback='parse_page',follow=True),
    )
    def parse_page(self,response):
        category = response.xpath("//div[@class='uibox']/div/text()").get()
        srcs = response.xpath("//div[contains(@class,'uibox-con')]/ul/li//img/@src").getall()
        srcs = list(map(lambda x:response.urljoin(x.replace("t_","")),srcs))
        yield BmwItem(category=category,image_urls=srcs)









    def test_parse(self, response):
=======
=======
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688

from bmw.items import BmwItem
class Bmw5Spider(scrapy.Spider):
    name = 'bmw5'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']

    def parse(self, response):
<<<<<<< HEAD
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
=======
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # for url in urls:
            #     # url = "https:"+url
            #     url = response.urljoin(url)
            #     print(url)
            urls =list(map(lambda url:response.urljoin(url),urls))
<<<<<<< HEAD
<<<<<<< HEAD
            item = BmwItem(category=category,image_urls=urls)
=======
            item = BmwItem(category=category,urls=urls)
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
=======
            item = BmwItem(category=category,urls=urls)
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
            yield item