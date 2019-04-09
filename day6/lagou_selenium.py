#encoding:utf-8

from selenium import webdriver
from lxml import etree
import re
import time
class LagouSpider(object):
    driver_path = dirver_path = r"C:\www\chromedriver\chromedriver.exe"
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.dirver_path)
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.positions = []
    def run(self):
        self.driver.get(self.url)
        source = self.driver.page_source
        # print(source)
        self.parse_list_page(source)
    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//a[@class='position_link']/@href")
        for link in links:
            #print(link)
            self.request_detail_page(link)
            time.sleep(2)
    def request_detail_page(self,url):
        #新建一个窗口 展示该职位的详细信息 并获取源代码
        #将源代码交给parse_detail_content 再获取详细内容
        self.driver.execute_script("window.open('%s')"%url)
        #selenium 虽然新建了一个页面 但是driver 并没由切换过去
        self.driver.switch_to_window(self.driver.window_handles[1])
        source = self.driver.page_source #获取详情页的源代码
        self.parse_detail_content(source)
    def parse_detail_content(self,source):
        pass
        #这里边 获取标题要求等详细内容
if __name__ == "__main__":
    spider = LagouSpider()
    spider.run()