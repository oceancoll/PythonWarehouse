# coding:utf-8
import pika

# 备份交换机
# 生产者如果不设置mandatory参数，消息在未被路由的情况下将会丢失
# 通过设置备份交换机，可以使没有路由的消息被统一存储到一个队列中

# 设置的方法：在创建direct类型的exchange时，增加alternate-exchange参数，指定备份的exchange
# 备份的exchange的类型需要是fanout，因为传入到原始direct类型的exchange数据的routing_key会保持不变
# 当备份的exchange设置为direct时，只有原始routing_key与备份routing_key相同时，才会接收到这个消息
# 如果设置为fanout类型，会全部接收消息

# 如果备份交换机和mandatory参数同时设置，那么mandatory参数将会失效

credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
args ={}
args['alternate-exchange'] = "myAE"
channel.exchange_declare(exchange='normalExchange', exchange_type='direct', arguments=args)
channel.exchange_declare(exchange='myAE', exchange_type='fanout')
channel.queue_declare(queue="normalQueue")
channel.queue_bind(queue="normalQueue", exchange='normalExchange', routing_key="normalKey")
channel.queue_declare(queue="unroutedQueue")
channel.queue_bind(queue="unroutedQueue", exchange='myAE', routing_key="")
# 有满足路由的routing_key
channel.basic_publish(exchange='normalExchange', routing_key='normalKey', body=str(1))
# 不满足条件的routing_key,会被写到备份交换机的队列中
channel.basic_publish(exchange='normalExchange', routing_key='eee', body=str(1))