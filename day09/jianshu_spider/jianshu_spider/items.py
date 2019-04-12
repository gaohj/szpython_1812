# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    avatar = scrapy.Field()
    author = scrapy.Field()
    pub_time = scrapy.Field()
    origin_url = scrapy.Field()
    article_id = scrapy.Field()
    content = scrapy.Field()

