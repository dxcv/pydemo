# -*- coding: utf-8 -*-
# @Time    : 2018/12/10 13:21
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : myproducer.py

import pika
credentials = pika.PlainCredentials('guest','guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',5672,'/',credentials))
channel = connection.channel()

# 声明queue
channel.queue_declare(queue='balance')

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='balance',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

#  p --> X --> Q --> c

# Exchange 交换器

# fanout类型的Exchange路由规则非常简单，它会把所有发送到该Exchange的消息路由到所有与它绑定的Queue中。


# direct类型的Exchange路由规则也很简单，它会把消息路由到那些binding key与routing key完全匹配的Queue中

#topic  前面提到的direct规则是严格意义上的匹配，换言之Routing Key必须与Binding Key相匹配的时候才将消息传送给Queue，
# 那么topic这个规则就是模糊匹配，可以通过通配符满足一部分规则就可以传送。它的约定是：
#routing key为一个句点号“. ”分隔的字符串（我们将被句点号“. ”分隔开的每一段独立的字符串称为一个单词），
# 如“stock.usd.nyse”、“nyse.vmw”、“quick.orange.rabbit” binding key与routing key一样也是句点号“. ”分隔的字符串
#binding key中可以存在两种特殊字符“*”与“#”，用于做模糊匹配，其中“*”用于匹配一个单词，“#”用于匹配多个单词（可以是零个）



# fanout   direct   topic
# routing_key   binding_key