# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boss.items import BossItem


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101280600/?query=python&page=1']

    rules = (
        #获取列表的规则
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d'),follow=True),
        #获取详情页的规则
        Rule(LinkExtractor(allow=r'.+job_detail/.+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        name = response.xpath("//h1/text()").get().strip()
        salary = response.xpath("//span[@class='salary']/text()").get().strip()
        job_info = response.xpath("//*[@id='main']/div[1]/div/div/div[2]/p//text()").getall()
        city = job_info[0]
        work_year = job_info[1]
        education = job_info[2]
        positon_info = response.xpath("//div[@class='job-sec']//div[1][@class='text']/text()").get()
        # # positon_info = "".join(positon_info).strip()
        company = response.xpath("//div[@class='company-info']//a[2]/text()").get().strip()
        item = BossItem(name=name,salary=salary,city=city,work_year=work_year,education=education,company=company,positon_info=positon_info)
        yield item

