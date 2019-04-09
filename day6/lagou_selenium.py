#encoding:utf-8

from selenium import webdriver
from lxml import etree
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
class LagouSpider(object):
    dirver_path = r"C:\www\chromedriver\chromedriver.exe"
    chromes_options = Options()
    chromes_options.add_argument("--headless") #不用打开浏览器 就可以进行爬取
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.dirver_path,chrome_options=LagouSpider.chromes_options)
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.positions = []
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            # 第一页完成以后 模拟人点击下一页
            WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[last()]"))

            )
            self.parse_list_page(source)
            # 如果没有下一页了 我们退出
            try:
                next_btn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
                if "pager_next_disabled" in next_btn.get_attribute("class"):
                    return
                else:
                    next_btn.click()
            except:
                print(source)
            time.sleep(2)
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
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='job-name']/span[@class='name']"))

        )
        source = self.driver.page_source #获取详情页的源代码
        self.parse_detail_content(source)
        self.driver.close() #关闭详情页
        self.driver.switch_to.window(self.driver.window_handles[0])
    def parse_detail_content(self,source):
        html = etree.HTML(source)
        #这里边 获取标题要求等详细内容
        position_name = html.xpath("/html/body/div[2]/div/div[1]/div/span/text()")[0]
        job_request = html.xpath("//dd[@class='job_request']//span")
        salary = job_request[0].xpath(".//text()")[0].strip()
        city = job_request[1].xpath(".//text()")[0].strip()
        city = re.sub(r"[\s/]","",city)
        work_years = job_request[2].xpath(".//text()")[0].strip()
        work_years = re.sub(r"[\s/]", "", work_years)
        education = job_request[3].xpath(".//text()")[0].strip()
        education = re.sub(r"[\s/]", "", education)
        desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
        company_name = html.xpath("//*[@id='job_company']/dt/a/div/h2/em/text()")[0].strip()
        position = {
            "position_name":position_name,
            "company_name":company_name,
            "salary":salary,
            "city":city,
            "work_years":work_years,
            "education":education,
            "desc":desc,

        }
        self.positions.append(position)
        print(position)
        print("="*100)



if __name__ == "__main__":
    spider = LagouSpider()
    spider.run()