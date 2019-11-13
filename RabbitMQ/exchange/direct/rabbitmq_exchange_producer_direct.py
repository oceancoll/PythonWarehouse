# coding:utf-8
# rabbitmq的发布与订阅需要借助交换机(Exchange)模式
# direct模式：路由模式，消息发送至exchange上，exchange根据路由键(routing_key)转发到相应的queue上
# 可以同时绑定多个routing_key，也就是说同一个key可以接收多个路由消息
# 需要先启动订阅者，这种模式下的队列是consumer随机生成的，发布者仅仅发布消息到exchange，由exchange转发消息至queue
# 模型图：https://images2018.cnblogs.com/blog/1348425/201809/1348425-20180909221806563-1440800238.png

import pika
import json

credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
# 创建一个exchange名为python-test2,类型为direct的exchange，可选参数durable=Ture是否持久化
channel.exchange_declare(exchange='python-test2', exchange_type='direct')
for i in range(10):
    message = json.dumps({'OrderId': "1000%s" % i})
    # 向队列插入数值 routing_key是队列名。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。
    # 可以同时发多组消息
    channel.basic_publish(exchange='python-test2', routing_key='OrderId', body=message)
    channel.basic_publish(exchange='python-test2', routing_key='OrderId1', body=message)
    print(message)
connection.close()
