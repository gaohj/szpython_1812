import json
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}


# 获取总页数
def get_page(url):
    response = requests.get(url, headers=headers)
    # print(response.text)

    mytree = etree.HTML(response.text)
    page_data = mytree.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0]
        # {"totalPage":100,"curPage":1}
    page_data_dict = json.loads(page_data)
    total_page = page_data_dict['totalPage']

    print(total_page)


if __name__ == '__main__':
    start_url = "https://sz.lianjia.com/ershoufang/"

    get_page(start_url)
