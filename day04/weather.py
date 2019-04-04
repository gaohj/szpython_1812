#pip install pyecharts

import requests
from bs4 import BeautifulSoup
def parse_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text,'lxml')
    conMidtab=soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for tr in trs:
            tds = tr.find_all('td')
            city_td = tds[0] #获取列表
            city = list(city_td.stripped_strings)[0]
            temp_ed = tds[-5]
            temp_max = list(temp_ed.stripped_strings)[0]
            print({"city":city,"max_temp":temp_max})
def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
    ]

    for url in urls:
        parse_page(url)

if __name__ == "__main__":
    main()