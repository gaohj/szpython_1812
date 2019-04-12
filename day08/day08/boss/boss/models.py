#encoding: utf-8
from datetime import datetime,timedelta
#timedelte 表示两个datetime的时间差

class ProxyModel(object):
    def __init__(self,data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.blacked = False

        date_str, time_str = self.expire_str.split(" ")
        year, month, day = date_str.split("-")
        hour, minute, second = time_str.split(":")
        self.expire_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute),
                             second=int(second))

        # https://ip:port
        self.proxy = "https://{}:{}".format(self.ip,self.port)

    @property #将下面的函数当成属性来调用
    def is_expiring(self):
        now = datetime.now()
        if (self.expire_time-now) < timedelta(seconds=5):
            return True
        else:
            return False