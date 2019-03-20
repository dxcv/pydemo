
# -*- coding:utf-8 -*-

# 数据只会放入到queue中,不会放入exchange中
#1.生产者只会往这个交换机通知;
#2.检查那些消费者,消费者绑定的queue中放入数据
#3.消费者获取queue中数据


from rbtmq.fanout_direct_topic.pikaUtil import pika , channel ,connection

channel.exchange_declare(exchange='important_notice1',exchange_type='fanout',durable=True)#创建一个fanout(广播)类型的交换机exchange。

message =  "广播信息,请打开收音机,错过就收不到了,不提供回放哦1"
confirmation =channel.basic_publish(exchange='important_notice1',
                                    routing_key='',
                                    body=message,
                                    properties=pika.BasicProperties(delivery_mode=2,) ,
                                    mandatory=False,
                                    immediate=False)
if confirmation :
    print('已成功提交至队列中')
connection.close()