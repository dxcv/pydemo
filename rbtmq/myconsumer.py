# -*- coding: utf-8 -*-
# @Time    : 2018/12/10 13:19
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : myconsumer.py

#消费者

import pika

credentials = pika.PlainCredentials('guest','guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',5672,'/',credentials))
channel = connection.channel()


channel.queue_declare(queue='balance')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue='balance',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()