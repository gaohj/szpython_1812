# -*- coding: utf-8 -*-
import scrapy
import re

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):

        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s","",province_text)
            if province_text:
                province = province_text
            if province == '其它':
                continue

            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # print("省份：%s,城市%s"%(province,city))
                # print("链接%s"%city_url)
            #构建新房的url
            #先对主站的url 进行切割 比如http://cqliangping.fang.com
            #https://hf.newhouse.fang.com/house/s/
                url_module = city_url.split("//")
                scheme = url_module[0]
                domain = url_module[1]
                city_new = domain.split(".")[0] #hf
                if 'bj.' in domain:
                    new_houseurl = 'https://newhouse.fang.com/house/s/'
                    esf_url = 'https://esf.fang.com/'
                else:
                    new_houseurl = scheme+"//"+city_new+".newhouse.fang.com/"+"house/s/"
                    esf_url = scheme+"//"+city_new+".esf.fang.com"
                #print("新房:%s,二手房:%s"%(new_houseurl,esf_url))

                yield scrapy.Request(url=new_houseurl,callback=self.parse_newhouse,meta={"info":(province,city)})
            #yield scrapy.Request(url=esf_url,callback=self.parse_esf,meta={"info":(province,city)})

    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            name= li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()

    def parse_esf(self):
        pass