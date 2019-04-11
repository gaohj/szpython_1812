# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request
<<<<<<< HEAD
<<<<<<< HEAD
from scrapy.pipelines.images import ImagesPipeline
from bmw import settings
=======
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
=======
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
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
<<<<<<< HEAD
<<<<<<< HEAD

class BMWImagesPipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #这个方法是在发送下载请求之前调用
        #也就是说这个方法 就是去发送下载请求
        requests_objs =super(BMWImagesPipline, self).get_media_requests(item,info)
        for requests_obj in requests_objs:
            requests_obj.item = item
        return requests_objs
    def file_path(self, request, response=None, info=None):
        #这个方法是在图片将要保存的时候调用 获取图片存储的路径
        path = super(BMWImagesPipline, self).file_path(request,response,info)
        #path返回的就是图片的路径
        #但是返回的是 full/asdfads.jpg
        category = request.item.get('category')
        #file_path仅仅是获取图片存储的路径 分类不能拿到  需要在发送请求之前拿到分类
        #需要重写get_media_requests 方法
        image_store = settings.IMAGES_STORE
        category_path = os.path.join(image_store,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/","") #图片的名字
        image_path = os.path.join(category_path,image_name)
        return image_path
=======
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
=======
>>>>>>> c7bd8bff104fbf41cb4953006ae4266c6b6df688
