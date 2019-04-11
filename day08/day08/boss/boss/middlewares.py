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

class IPProxyDownloadMiddleware(object):

    PROXY_URL = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='

    def __init__(self):
        super(IPProxyDownloadMiddleware, self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self,request,spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            # 请求代理
            self.update_proxy()

        request.meta['proxy'] = self.current_proxy.proxy

    def process_response(self,request,response,spider):
        if response.status != 200 or "captcha" in response.url:
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            print('%s这个代理被加入黑名单了'%self.current_proxy.ip)
            self.update_proxy()
            # 如果来到这里，说明这个请求已经被boss直聘识别为爬虫了
            # 所有这个请求就相当于什么都没有获取到
            # 如果不返回request，那么这个request就相当于没有获取到数据
            # 也就是说，这个请求就被废掉了，这个数据就没有被抓取到
            # 所有要重新返回request，让这个请求重新加入到调度中，
            # 下次再发送
            return request
        # 如果是正常的，那么要记得返回response
        # 如果不返回，那么这个resposne就不会被传到爬虫那里去
        # 也就得不到解析
        return response

    def update_proxy(self):
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            print('重新获取了一个代理：',text)
            result = json.loads(text)
            if len(result['data']) > 0:
                data = result['data'][0]
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
        self.lock.release()

