# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 10:34
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : amq.py


import stomp
import time

queue_name = '/queue/SampleQueue'
topic_name = '/topic/SampleTopic'
listener_name = 'SampleListener'

host = '192.168.1.233'
post = 61613
user = 'admin'
password = 'admin'




class SampleListener(object):
    def on_message(self, headers, message):
        print ('headers: %s' % headers)
        print ('message: %s' % message)


# 推送到队列queue
def send_to_queue(msg):
    conn = stomp.Connection10([(host, post)])
    conn.start()
    conn.connect()
    conn.send(queue_name, msg)
    conn.disconnect()


# 推送到主题
def send_to_topic(msg):
    conn = stomp.Connection10([(host, post)])
    conn.start()
    conn.connect()
    conn.send(topic_name, msg)
    conn.disconnect()


##从队列接收消息
def receive_from_queue():
    conn = stomp.Connection10([(host, 61613)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(queue_name)
    time.sleep(1)  # secs
    conn.disconnect()


##从主题接收消息
def receive_from_topic():
    conn = stomp.Connection10([(host, post)])
    conn.set_listener(listener_name, SampleListener())
    conn.start()
    conn.connect()
    conn.subscribe(topic_name)
    while 1:
        send_to_topic('topic')
        time.sleep(3)  # secs
    conn.disconnect()


if __name__ == '__main__':
    send_to_queue('len 123')
    receive_from_queue()
    # send_to_topic('len 345')
    # receive_from_topic()