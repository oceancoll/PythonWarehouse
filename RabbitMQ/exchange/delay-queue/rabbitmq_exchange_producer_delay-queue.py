# coding:utf-8
import pika
import json

# 延迟队列
# rabbitmq本身不支持延迟队列，通过死亡交换机和死亡键来实现
# 实现了5-60s的分别延迟队列
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, 'test_vhost', credentials))
# 创建频道
channel = connection.channel()
channel.exchange_declare(exchange='dlx-exchange', exchange_type='direct')
channel.queue_declare(queue='dead_queue_5s')
channel.queue_declare(queue='dead_queue_10s')
channel.queue_declare(queue='dead_queue_30s')
channel.queue_declare(queue='dead_queue_60s')
channel.queue_bind(queue='dead_queue_5s', exchange='dlx-exchange', routing_key='routingkey.dead.5s')
channel.queue_bind(queue='dead_queue_10s', exchange='dlx-exchange', routing_key='routingkey.dead.10s')
channel.queue_bind(queue='dead_queue_30s', exchange='dlx-exchange', routing_key='routingkey.dead.30s')
channel.queue_bind(queue='dead_queue_60s', exchange='dlx-exchange', routing_key='routingkey.dead.60s')
channel.exchange_declare(exchange='common-exchange', exchange_type='direct')
arg5 = {'x-message-ttl': 5000}
arg10 = {'x-message-ttl': 10000}
arg30 = {'x-message-ttl': 30000}
arg60 = {'x-message-ttl': 60000}
arg5['x-dead-letter-exchange'] = 'dlx-exchange'
arg5['x-dead-letter-routing-key'] = 'routingkey.dead.5s'
arg10['x-dead-letter-exchange'] = 'dlx-exchange'
arg10['x-dead-letter-routing-key'] = 'routingkey.dead.10s'
arg30['x-dead-letter-exchange'] = 'dlx-exchange'
arg30['x-dead-letter-routing-key'] = 'routingkey.dead.30s'
arg60['x-dead-letter-exchange'] = 'dlx-exchange'
arg60['x-dead-letter-routing-key'] = 'routingkey.dead.60s'
channel.queue_declare(queue='common_queue_5s', arguments=arg5)
channel.queue_declare(queue='common_queue_10s', arguments=arg10)
channel.queue_declare(queue='common_queue_30s', arguments=arg30)
channel.queue_declare(queue='common_queue_60s', arguments=arg60)
channel.queue_bind(queue='common_queue_5s', exchange='common-exchange', routing_key='routingkey.common.5s')
channel.queue_bind(queue='common_queue_10s', exchange='common-exchange', routing_key='routingkey.common.10s')
channel.queue_bind(queue='common_queue_30s', exchange='common-exchange', routing_key='routingkey.common.30s')
channel.queue_bind(queue='common_queue_60s', exchange='common-exchange', routing_key='routingkey.common.60s')
for i in range(1,5,1):
    if i == 1:
        channel.basic_publish(exchange='common-exchange', routing_key='routingkey.common.5s', body=str(i))
    elif i == 2:
        channel.basic_publish(exchange='common-exchange', routing_key='routingkey.common.10s', body=str(i))
    elif i == 3:
        channel.basic_publish(exchange='common-exchange', routing_key='routingkey.common.30s', body=str(i))
    elif i == 4:
        channel.basic_publish(exchange='common-exchange', routing_key='routingkey.common.60s', body=str(i))



