# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request
class BmwPipeline(object):

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        # bmw/images
    def process_item(self, item, spider):
        category =item['category']
        urls =item['urls']
        #在images 中新建多个小目录
        category_path = os.path.join(self.path,category)
        #bmw/images/车身改装
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls: #遍历item 中 所有的图片url 截取其中的图片名 #然后下载到指定的目录
            img_name= url.split('_')[-1]
            request.urlretrieve(url,os.path.join(category_path,img_name))
        # bmw/images/车身改装/adfdasf.jpg
        return item
