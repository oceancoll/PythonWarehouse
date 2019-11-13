# coding:utf-8
# 公平调度模式
# 通过exchange的direct模式发送消息时，可以指定queue，并将exchange,routing_key,queue进行绑定

import pika
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
# 声明消息队列
channel.queue_declare(queue='hello3')
# 声明exchange
channel.exchange_declare(exchange='queue.work', exchange_type='direct')
# 绑定queue, exchange, routing_name
channel.queue_bind('hello3', 'queue.work', 'task')
# 向队列插入数值 routing_key是队列名 body是要插入的内容
for i in range(30):
    channel.basic_publish(exchange='queue.work', routing_key='task', body=str(i))
print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
connection.close()
