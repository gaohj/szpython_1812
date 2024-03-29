# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem,ESFHouseItem
from scrapy_redis.spiders import RedisSpider
class SfwSpider(RedisSpider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    #start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang:start_urls"
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
                # print("省份", province)
                # print("城市", city)
                # print("城市url", city_url)
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
                    # print("城市：%s%s" %(province, city))
                    # print("新房：%s" % new_houseurl)
                    #print("二手房：%s" % esf_url)

                yield scrapy.Request(url=new_houseurl,callback=self.parse_newhouse,meta={"info":(province,city)})

                yield scrapy.Request(url=esf_url,callback=self.parse_esf,meta={"info":(province,city)})
            #     break
            # break


    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get()
            if name is not None:
                name=name.strip()

            house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            # print(house_type_list)
            # break
            house_type_list = list(map(lambda x: re.sub(r"\s", "", x), house_type_list))
            rooms = list(filter(lambda x: x.endswith("居"), house_type_list))#几居
            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|－|/", "", area) #面积
            # print(area)
            # break
            address = li.xpath(".//div[@class='address']/a/@title").get()
            # print(address) 地址
            # break
            district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())#位于哪个区 //获取所有内容
            # [南山区] 啊是的撒的发生地方撒地方撒饭
            #截取位于哪个区
            district = re.search(r".*\[(.+)\].*", district_text)
            #匹配中括号
            if district:
                district = "".join(district.groups(1))
            sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            #看是否在销售状态还是 待售等
            # print(sale)
            # break
            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s|广告", "", price)
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            #楼盘详情链接
            # print(origin_url)
            item = NewHouseItem(name=name, rooms=rooms, area=area, address=address, district=district, sale=sale,
                                price=price, origin_url=origin_url, province=province, city=city)
            yield item

        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_newhouse,
                                 meta={"info": (province, city)})

    def parse_esf(self, response):
        province, city = response.meta.get('info')
        dls = response.xpath("//div[contains(@class,'shop_list')]/dl")
        for dl in dls:
            item = ESFHouseItem(province=province, city=city)
            item['name'] = dl.xpath(".//p[@class='add_shop']/a/@title").get()

            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x: re.sub(r"\s", "", x), infos))
            for info in infos:
                if "厅" in info:
                    item['rooms'] = info
                    #print(item['rooms'])
                elif '层' in info:
                    item['floor'] = info
                elif '向' in info:
                    item['toward'] = info
                elif '㎡' in info:
                    item['area'] = info
                elif '年建' in info:
                    item['year'] = info
                else:
                    pass
            item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            item['price'] = "".join(dl.xpath(".//dd[@class='price_right']/span[1]//text()").getall())
            item['unit'] = "".join(dl.xpath(".//dd[@class='price_right']/span[2]/text()").getall())
            detail_url = dl.xpath(".//h4[@class='clearfix']/a/@href").get()
            item['origin_url'] = response.urljoin(detail_url)
            yield item
        next_url = response.xpath("//a[@id='PageControl1_hlk_next']/@href").get()
        yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf, meta={"info": (province, city)})
