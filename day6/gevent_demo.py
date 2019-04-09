import gevent

#gevent +sleep 谁睡眠时间短 或者此刻谁没睡眠  就把 cpu的执行权给哪个协程
def f1():
    gevent.sleep(1)
    print("协程1开始")
    gevent.sleep(1)
    print("协程1结束")
def f2():
    gevent.sleep(3)
    print("协程2开始")

    gevent.sleep(3)
    print("协程2结束")

def f3():
    gevent.sleep(5)
    print("协程3开始")

    gevent.sleep(5)
    print("协程3结束")

if __name__ == "__main__":
    g1 = gevent.spawn(f1)
    g2 = gevent.spawn(f2)
    g3 = gevent.spawn(f3)

    # g1.join()
    # g2.join()
    # g3.join()

    gevent.joinall([g1,g2,g3])