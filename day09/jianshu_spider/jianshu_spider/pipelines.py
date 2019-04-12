# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql import cursors #导入游标类
from twisted.enterprise import adbapi
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
        self.cursor.execute(self.sql,(item['title'],item['content'],item['avatar'],item['author'],item['pub_time'],item['origin_url'],item['article_id']))
        self.conn.commit()
        return item
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,avatar,author,pub_time,origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s,%s)
            
            """
            return self._sql
        return self._sql

#scrapy 使用Twisted 进行异步IO
class JianshuTwistedSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'123456',
            'database':'jianshu6',
            'charset':'utf8',
            'cursorclass':cursors.DictCursor
        }

        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
               insert into article(title,content,avatar,author,pub_time,origin_url,article_id,read_count,like_count,word_count,comment_count,subjects) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

               """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item,item) #异步操作
        defer.addErrback(self.handle_error,item, spider)
        #真正执行  和抛出错误需要另外的两个方法
    def insert_item(self,cursor,item):
        print(item['read_count'],item['like_count'],item['word_count'],item['comment_count'])
        cursor.execute(self.sql,(item['title'], item['content'], item['avatar'], item['author'], item['pub_time'], item['origin_url'],item['article_id'],item['read_count'],item['like_count'],item['word_count'],item['comment_count'],item['subjects']))

    def handle_error(self,error,item,spider):
        print("="*20+"error"+"="*20)
        print(error)
        print("=" * 20 + "error" + "=" * 20)