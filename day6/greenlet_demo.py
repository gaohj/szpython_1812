from greenlet import greenlet
import time

def f1():
    print('男人最害怕哪一天?很明显1月31日')
    time.sleep(2)

    print("种花多没意思,我们一起种草莓")
    time.sleep(3)
    g2.switch()
def f2():
    print('2错过我过了这个村,我在下个村口等你')
    time.sleep(2)
    g1.switch() #把cpu的执行全交给 g1 协程


if __name__ == "__main__":
    g1 = greenlet(f1)
    g2 = greenlet(f2)
    g2.switch()