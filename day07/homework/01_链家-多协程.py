import gevent
from gevent import monkey
gevent.monkey.patch_all()

import time
import requests
from lxml import etree


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}


# 获取当前区中的所有房源
def get_house(url, name):

    response = requests.get(url, headers=headers)
    html = response.text
    # print(html)

    # 处理数据
    mytree = etree.HTML(html)

    house_list = mytree.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGCLICKDATA"]')
    # print(house_list)

    for house in house_list:
        # 房源标题
        title = house.xpath('.//div[@class="info clear"]/div[@class="title"]/a/text()')[0]
        # 房子价格
        price = house.xpath('.//div[@class="info clear"]/div[@class="priceInfo"]/div[1]/span/text()')[0]

        # print(name, title, price)

        # 持久化存储
        # 存入文件
        print(name)
        with open("sz/%s.txt"%name, 'a+', encoding='utf-8') as fp:
            fp.write(str((name, title, price)) + "\n")
            fp.flush()


# 获取所有区
def get_areas(start_url):

    response = requests.get(start_url, headers=headers)
    html = response.text

    mytree = etree.HTML(html)

    area_list = mytree.xpath('//div[@data-role="ershoufang"]/div/a')
    # print(area_list)

    a_list = []
    for area in area_list:
        name = area.xpath('./text()')[0]  # 区名
        area_url = area.xpath('./@href')[0]  # 区url
        area_url = "https://sz.lianjia.com" + area_url
        # print(name, area_url)

        a_dict = {"name": name, "url": area_url}
        a_list.append(a_dict)

    return a_list


if __name__ == '__main__':
    start_url = "https://sz.lianjia.com/ershoufang/"

    # 获取所有区的区名和区url
    a_list = get_areas(start_url)

    time.clock()

    # 针对每个区开启一个线程
    g_list = []
    for area in a_list:
        name = area.get("name")  # 区名
        url = area.get("url")  # url

        # 异步
        # 创建协程
        g = gevent.spawn(get_house, url, name)

        g_list.append(g)

    gevent.joinall(g_list)


    # 执行时间
    print(time.clock())

