import gevent


def fn1():
    gevent.sleep(1)
    print("协程1")

    gevent.sleep(9)
    print("协程1结束")

def fn2():
    gevent.sleep(3)
    print("协程2")

    gevent.sleep(5)
    print("协程2结束")


def fn3():
    gevent.sleep(5)
    print("协程3")

    gevent.sleep(1)
    print("协程3结束")


if __name__ == '__main__':
    g1 = gevent.spawn(fn1)
    g2 = gevent.spawn(fn2)
    g3 = gevent.spawn(fn3)

    gevent.joinall([g1])


