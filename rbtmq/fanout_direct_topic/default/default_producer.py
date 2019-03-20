
# -*- coding:utf-8 -*-

from rbtmq.fanout_direct_topic.pikaUtil import pika,channel ,connection
import random

#个人觉得没必要申明
# channel.queue_declare(queue='test_fanout')  #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行

mobile = "1521688861"+str(random.randint(1,10))

confirmation =channel.basic_publish(exchange='',
                                    routing_key='test_default',#写明将消息发往哪个队列，本例是将消息发往队列
                                    body=mobile,
                                    properties=pika.BasicProperties(delivery_mode=2,) ,# make message persistent=>使消息持久化的特性
                                    mandatory=False,
                                    immediate=False)
if confirmation :
    print('已成功提交至队列中')
connection.close()