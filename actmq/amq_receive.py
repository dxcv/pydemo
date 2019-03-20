# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 10:53
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : amq_receive.py




import stomp
import time

listener_name = 'SampleListener'

host = '192.168.1.234'
post = 61613
user = 'admin'
password = 'admin'


class SampleListener(object):
    def on_message(self, headers, message):
        print ('headers: %s' % headers["destination"])
        print ('message: %s' % message)

##从队列接收消息
def receive_from_queue():
    conn = stomp.Connection10([(host, 61613)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect(user, password, wait=True)
    conn.subscribe('/queue/SampleQueue')
    time.sleep(1)  # secs
    conn.disconnect()



##从主题接收消息
def receive_from_topic():
    conn = stomp.Connection10([(host, post)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect(user, password, wait=True)
    conn.subscribe('/topic/SampleTopic')
    while 1:
        time.sleep(3)  # secs
    conn.disconnect()


if __name__ == '__main__':
    receive_from_topic()