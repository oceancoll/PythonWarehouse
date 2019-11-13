# coding:utf-8
# rabbitmq的发布与订阅需要借助交换机(Exchange)模式
# fanout模式：传递到exchange的消息都会转发到所有与其绑定的queue上
# 也就是说这种模式下，所有绑定了该exchange的地方都会收到消息
# 不需要指定routing_key,即使指定了也无效
# 需要先启动订阅者，这种模式下的队列是consumer随机生成的，发布者仅仅发布消息到exchange，由exchange转发消息至queue
# 每个consumer在启动时都会生成一个随机队列
# 模型图：https://img-blog.csdnimg.cn/2019102916413736.png



# Q1: 服务端没有声明queue，为什么客户端要声明一个queue?
# A1: 生产者负责将消息发送到exchange上，exchange会遍历一遍，绑定了哪些queue，把消息发送到queue里面(这是为什么要先启动消费者)
#     消费者只会从queue中读消息，exchange不会直接把消息发送给消费者，这就是为什么要有queue的存在

# Q2: 为什么queue要自动生成，而不是自己手动去写?
# A2: queue的存在是为了收广播的，如果消费者不接收了，则queue就没有存在的必要了，于是就自动生成，自动销毁

# 广播的实时性：广播是实时的，当生产者发消息时，消费者不存在就收不到消息。成为发布订阅，又称收音机模式

import pika
import json
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
# 创建一个exchange名为python-test1,类型为fanout的exchange，可选参数durable=Ture是否持久化
channel.exchange_declare(exchange='python-test1', exchange_type='fanout')
for i in range(10):
    message=json.dumps({'OrderId':"1000%s"%i})
    # 向队列插入数值 routing_key是队列名。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。routing_key 不需要配置
    # channel.basic_publish(exchange = 'python-test',routing_key = '',body = message,
    #  properties=pika.BasicProperties(delivery_mode = 2))
    channel.basic_publish(exchange='python-test1', routing_key='', body=message)
    print(message)
connection.close()
