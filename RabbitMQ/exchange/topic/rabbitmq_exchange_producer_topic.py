# coding:utf-8
# rabbitmq的发布与订阅需要借助交换机(Exchange)模式
# topic模式：传递到exchange的消息都会转发到routing_key模式满足的queue上
# 需要先启动订阅者，这种模式下的队列是consumer随机生成的，发布者仅仅发布消息到exchange，由exchange转发消息至queue
# 每个consumer在启动时都会生成一个随机队列
# 模型图：https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcxMTI2MTcwMDI3NzU4

# 匹配规则
# ha.*.*
# ha.#
# .用来分隔单词，一个*匹配一个单词，#匹配多个单词

import pika
import json
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
# 创建一个exchange名为python-test1,类型为topic的exchange，可选参数durable=Ture是否持久化
channel.exchange_declare(exchange='python-test3', exchange_type='topic')
for i in range(10):
    message=json.dumps({'OrderId':"1000%s"%i})
    channel.basic_publish(exchange='python-test3',routing_key='ha.ga.ef',body=message)
    print(message)
connection.close()
