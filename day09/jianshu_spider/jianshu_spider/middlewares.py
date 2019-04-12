import random
import json
import requests
from twisted.internet.defer import DeferredLock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from scrapy.http.response.html import HtmlResponse
class UserAgentDownloadMiddleware(object):
    USER_AGENTS = [
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1'
    ]

    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        # self.options.add_argument("--proxy-server:http://ip:端口号")
        self.driver = webdriver.Chrome(r'C:\www\chromedriver\chromedriver.exe',chrome_options=self.options)

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                showMore =self.driver.find_element_by_class_name('show-more')
                showMore.click()
                time.sleep(0.5)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        #截获请求让chrome去发送 然后再返回
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response