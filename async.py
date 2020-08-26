# -*- coding:utf-8 -*-
'''
@author: miyao
@time: 2020/8/24
'''
import sys
from threading import Thread
from time import sleep

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def A():
    sleep(2)
    print("函数A睡了2秒钟。。。。。。")
    print("a function")


def B():
    print("b function")


if __name__ == '__main__':
    A()
    B()
