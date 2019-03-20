
# -*- coding:utf-8 -*-
# 持续消费

from rbtmq.fanout_direct_topic.pikaUtil import  pika ,channel
import time

def consumer_callback(channel, method, properties, body):
    '''
    :param channel: BlockingChannel
    :param method:  spec.Basic.Deliver
    :param properties: spec.BasicProperties
    :param body:  str or unicode
    :return:
    '''
    assert isinstance(channel, pika.adapters.blocking_connection.BlockingChannel)
    # time.sleep(160)
    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
    print( body)


channel.exchange_declare(exchange='direct_log',exchange_type='direct')
#exclusive=True 跟 durable=True 不能同时设置
#exclusive=True 消费者只有线程存在的前提下收到消息,不存在就收不到,所以就不能持久化了
queue_declare = channel.queue_declare(queue="direct_queue_log1",durable=True)
# queue_name = queue_declare.method.queue #不能用这个随机的名字,会生成很多queue

severities = ['info','err']
for severity  in severities:
    channel.queue_bind(exchange='direct_log',queue='direct_queue_log1',routing_key=severity)

channel.basic_consume(consumer_callback =consumer_callback , queue="direct_queue_log1" ,no_ack = False )
channel.start_consuming()
