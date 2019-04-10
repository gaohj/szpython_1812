# -*- coding: utf-8 -*-
import scrapy
from day07.qsbk.qsbk.items import  QsbkItem
from scrapy.selector.unified import SelectorList
from scrapy.http.response.html import HtmlResponse
class QsbkDemoSpider(scrapy.Spider):
    name = 'qsbk_demo' #项目的名称
    allowed_domains = ['qiushibaike.com']#只能从这个域名爬取
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = "https://www.qiushibaike.com"
    #开始的域名
    def parse(self, response):
        duanzi_divs = response.xpath("//div[@id='content-left']/div")
        # print("="*100)
        # print(type(duanzidivs))
        # print("="*100)
        #get 将内容转成 Unicode编码 并提取出来
        for dz in duanzi_divs:
            author = dz.xpath(".//h2/text()").get().strip()
            content = dz.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            #数据解析回来  我们要交给pipline去处理 我们可以使用yield 收集信息 然后统一return返回
            item = QsbkItem(author=author,content=content)
            yield item #将函数变成生成器 接下来遍历生成器 然后将信息一个个的返回回去
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)