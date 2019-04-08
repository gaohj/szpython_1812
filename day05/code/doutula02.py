#encoding:utf-8

import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading

class ProducerTread(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(ProducerTread.self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self): #run() 来解析我们的init
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get() #从队列中取出每个页面的url
            self.parse_page(url) #然后调用parse_page 下载每个表情的url 并将它放到img_queue
            #队列中


    def parse_page(self,url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt')
            alt = re.sub(r'[?\？。\.,，。！!]', '', alt)
            suffix = os.path.splitext(img_url)[1]
            filename = alt+suffix
            self.img_queue.put((img_url,filename))
class CustomerTread(threading.Thread):
    def run(self):
        pass


def main():
    #实例化两个队列
    page_queue = Queue(50) #爬取50页
    img_queue = Queue(1000) #表情
    for x in range(1,51):
        url = 'http://www.doutula.com/photo/list/?page=%d'% x
        page_queue.put(url) #将每一页的url地址放到队列中
    for x in range(5):
        t= ProducerTread(page_queue,img_queue)
        t.start()
    for x in range(5):
        t=CustomerTread(page_queue,img_queue)
        t.start()
if __name__ == "__main__":
    main()