
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
    time.sleep(20)
    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False) #手动设置 ，只有 no_ack =False 时才有用
    print("调用发送短信接口,手机号码： %s" % body)


channel.queue_declare(queue='test_default',durable=True ) #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行

#公平调度。在一个消费者未处理完一个消息之前不要分发新的消息给它，
# 而是将这个新消息分发给另一个不是很忙的消费者进行处理。
# 为了解决这个问题我们可以在消费者代码中使用 channel.basic.qos ( prefetch_count = 1 )，将消费者设置为公平调度。
channel.basic_qos(prefetch_count=1)

#设置no_ack = False 手动处理(channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False))
channel.basic_consume(consumer_callback =consumer_callback , queue='test_default' ,no_ack = False )
channel.start_consuming()
