
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
    # time.sleep(20)
    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False) #手动设置 ，只有 no_ack =False 时才有用
    print( body)


channel.exchange_declare(exchange='important_notice1',exchange_type='fanout',durable=True)
#创建一个队列，exclusive=True（唯一性）表示在消费者与rabbitmq断开连接时，该队列会自动删除掉。
queue_declare = channel.queue_declare(exclusive=True)
#因为rabbitmq要求新队列名必须是与现存队列名不同，所以为保证队列的名字是唯一的，method.queue方法会随机创建一个队列名字，如：‘amq.gen-JzTY20BRgKO-HjmUJj0wLg‘。
queue_name = queue_declare.method.queue
channel.queue_bind(exchange='important_notice1',queue=queue_name) #会产生一个queue

channel.basic_consume(consumer_callback =consumer_callback , queue=queue_name ,no_ack = False )
channel.start_consuming()
