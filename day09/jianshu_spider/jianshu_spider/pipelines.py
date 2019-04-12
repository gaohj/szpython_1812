# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class JianshuSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'123456',
            'database':'jianshu6',
            'charset':'utf8'
        }
        #** 代表将字典中的key 和value当作关键字传过去
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None
    def process_item(self, item, spider):
        pass
    @property
    def sql(self):
        return self._sql