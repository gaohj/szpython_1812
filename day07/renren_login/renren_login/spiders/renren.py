# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']
    # else: start_requests 默认从start_urls 遍历所有的链接  发送request 默认get 请求
    # for url in self.start_urls:
    #     yield Request(url, dont_filter=True)
    #我们想发送post请求 那么必须 重新 start_requests
    def start_requests(self):
        url = "http://www.renren.com/PLogin.do"
        data = {"email":"gaohj5@163.com","password":"12qwaszx"}
        request = scrapy.FormRequest(url,formdata=data,callback=self.parse_page)
        yield request

    def parse_page(self, response):
        request = scrapy.Request(url="http://www.renren.com/541197383/profile",callback=self.parse_profile)
        yield request
    def parse_profile(self, response):
        with open("ghj.html",'w',encoding='utf-8') as fp:
            fp.write(response.text)