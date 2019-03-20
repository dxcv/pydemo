
# -*- coding:utf-8 -*-
#https://www.cnblogs.com/xiangjun555/articles/7873690.html

import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials))
channel = connection.channel()
assert isinstance(channel, pika.adapters.blocking_connection.BlockingChannel)
