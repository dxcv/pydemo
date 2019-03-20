
# -*- coding:utf-8 -*-
# 不用创建队列

from rbtmq.fanout_direct_topic.pikaUtil import pika , channel ,connection

channel.exchange_declare(exchange='direct_log',exchange_type='direct')

message =  '我要报告一个错误'
confirmation =channel.basic_publish(exchange='direct_log',
                                    routing_key='err',
                                    body=message,
                                    properties=None ,
                                    mandatory=False,
                                    immediate=False)
if confirmation :
    print('已成功提交至队列中')
connection.close()