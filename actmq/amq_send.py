# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 10:38
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : amq_send.py

import stomp
import time


host = '192.168.1.234'
post = 61613
user = 'admin'
password = 'admin'

#queue
def send_to_queue(msg):
    conn = stomp.Connection10([(host, post)])
    conn.start()
    conn.connect(user, password, wait=True)
    conn.send(destination='/queue/SampleQueue', body=msg)
    conn.disconnect()

#主题
def send_to_topic(msg):
    conn = stomp.Connection10([(host, post)])
    conn.start()
    conn.connect(user, password, wait=True)
    conn.send(destination='/topic/SampleTopic', body=msg)
    conn.disconnect()


if __name__ == '__main__':
    send_to_topic('len 123')
