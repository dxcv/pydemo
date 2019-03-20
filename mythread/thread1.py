# -*- coding: utf-8 -*-
# @Time    : 2019/1/14 11:18
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : thread1.py


import threading
import time

def run(n):
    print("task", n)
    time.sleep(1)
    print('2s')
    time.sleep(1)
    print('1s')
    time.sleep(1)
    print('0s')
    time.sleep(1)


class MyThread(threading.Thread):

    def __init__(self,name):
        print("--------:",name)
        super.__init__(MyThread)

    def run(self):
        print("t------")
        time.sleep(3)
        print("xxxxxxx")

if "__main__" == __name__:
    # t1 = threading.Thread(target=run, args=("t1",))
    # t2 = threading.Thread(target=run, args=("t2",))
    # t1.start()
    # t2.start()
    # t3=threading.Thread(target=run,args=("aaa",))
    # t3.start()

    '''GIL'''


    t=MyThread("thread1---")
    # t.setDaemon(True)
    print(t.getName())

    t2 = MyThread("thread2---")
    print(t2.getName())


    t.start()
    t2.start()
    t.join()

    # print( threading.active_count() )

