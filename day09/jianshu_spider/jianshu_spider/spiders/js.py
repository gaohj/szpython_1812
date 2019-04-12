# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']
    #https://www.jianshu.com/p/7014520ff562?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation
    #https://www.jianshu.com/p/10874f05df9a
    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        avatar = response.xpath("//a[@class='avatar']/img/@src").get()
        author = response.xpath("//span[@class='name']/a/text()").get()
        pub_time = response.xpath("//span[@class='publish-time']/text()").get().replace('*','')
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split("/")[-1]
        content = response.xpath("//div[@class='show-content']").get()
        item = ArticleItem(
            title=title,
            avatar=avatar,
            author=author,
            pub_time=pub_time,
            origin_url = response.url,
            article_id = article_id,
            content=content,
        )
        yield item