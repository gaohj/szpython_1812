import random
import json
import requests
from boss.models import ProxyModel
from twisted.internet.defer import DeferredLock
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

class IpProxyMiddleware(object):
    PROXY_URL = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    def __init__(self):
        super(IpProxyMiddleware, self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        #引擎发送给下载器之前调用
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            self.update_proxy()
        request.meta['proxy'] = self.current_proxy.proxy
        #这个proxy就是  # https://ip:port
    def process_response(self, request,response,spider):
        if response.status != 200 or 'captcha'in response.url:
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            print("%s ip被封锁" % self.current_proxy.proxy)
            self.update_proxy()
            #如果走到这里说明 被识别为爬虫
            #所以说这个请求就是什么都没有获取到
            #这个时候我们应该返回request 也就是说要重新进行下载
            return request
        return response
        #如果是正常的 记得返回response
        #如果不返回 传不到爬虫 也就是说得不到解析

    def update_proxy(self):
        #scrapy爬取的时候用的twisted 也就是异步 可以理解成多线程
        #如果异步都来请求代理造成IP浪费 处于节约IP的目的 异步上锁
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            print("重新获取了一个代理",text)
            result = json.loads(text)
            #芝麻代理不能让你频繁请求  也就是说 返回的data  可能没有值
            if len(result['data'])>0:
                data = result['data'][0] #{'ip': '106.46.136.7', 'port': 4225, 'expire_time': '2019-04-12 09:46:28'}
                #因为我们需要对data 进行多个操作 比如ip 和端口号拼接 时间转化成datetime类型判断是否过期
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
        self.lock.release()