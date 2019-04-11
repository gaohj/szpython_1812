# -*- coding: utf-8 -*-
import scrapy
import json

class HttpbinUseragentSpider(scrapy.Spider):
    name = 'httpbin_useragent'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        useragents =json.loads(response.text)['user-agent']
        print("="*30)
        print(useragents)
        print("="*30)
        #默认scrapy有去重功能 一个url 一旦请求过 就不会再请求
        #dont_filter 表示不过滤  允许继续请求该url
        yield scrapy.Request(self.start_urls[0],dont_filter=True)
