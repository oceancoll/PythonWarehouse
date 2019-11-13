# coding:utf-8
# exchange下的topic模式消费者
import pika
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182',5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='python-test3', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
# 匹配规则
# ha.*.*
# ha.#
# .用来分隔单词，一个*匹配一个单词，#匹配多个单词
# channel.queue_bind(exchange='python-test3', queue=queue_name, routing_key='ha.*.*')
channel.queue_bind(exchange='python-test3', queue=queue_name, routing_key='ha.#')
print(' [*] Waiting for logs. To exit press CTRL+C')
# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    "回调函数"
    print("[X] {0}".format(body))
channel.basic_consume(queue_name,callback, auto_ack=True)
channel.start_consuming()