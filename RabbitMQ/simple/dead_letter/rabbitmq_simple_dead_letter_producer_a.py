# coding:utf-8
# 死亡键，死亡路由
import pika
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
# arguments中，
#       x-message-ttl:整个队列中消息过期时间，单位为ms.
#       x-expires:当多长时间没有消费者访问该队列的时候，该队列会自动删除
#       x-max-length:队列的最大长度,当超过4条消息，前面的消息将被删除，给后面的消息腾位
#       x-max-length-bytes:指定队列存储消息的占用空间大小，当达到最大值是会删除之前的数据腾出空间
#       x-max-priority:设置消息的优先级，优先级值越大，越被提前消费
#       x-dead-letter-exchange,x-dead-letter-routing-key:死亡交换机,死亡路由键,
#           当队列中的消息过期，或者达到最大长度而被删除，或者达到最大空间时而被删除时
#           可以将这些被删除的信息推送到其他交换机中，让其他消费者订阅这些被删除的消息，处理这些消息
# channel.queue_declare(queue='hello4', durable=True,
#   arguments={'x-message-ttl': 10000, 'x-expires': 10000, 'x-max-length': 4, 'x-max-length-bytes':1024,
#   'x-max-priority':10})
channel.exchange_declare(exchange='exchange.dead', exchange_type='direct')
channel.queue_declare(queue='queue_dead')
channel.queue_bind(queue='queue_dead', exchange='exchange.dead', routing_key='routingkey.dead')
channel.exchange_declare(exchange='exchange.fanout', exchange_type='fanout')
# 设置各种参数
arguments = {}
# 统一设置队列中的所有消息的过期时间
arguments['x-message-ttl'] = 30000
# 设置超过多少毫秒没有消费者来访问队列，就删除队列的时间
arguments['x-expires'] = 20000
# 设置队列的最新的N条消息，如果超过N条，前面的消息将从队列中移除掉
arguments['x-max-length'] = 4
# 设置队列的内容的最大空间，超过该阈值就删除之前的消息
arguments['x-max-length-bytes'] = 1024
# 将删除的消息推送到指定的交换机
arguments['x-dead-letter-exchange'] = 'exchange.dead'
# 将删除的消息推送到指定的交换机对应的路由键
arguments['x-dead-letter-routing-key'] = 'routingkey.dead'
# 设置消息的优先级，优先级大的优先被消费
arguments['x-max-priority'] = 10
channel.queue_declare(queue='queue_name',arguments=arguments)
channel.queue_bind(queue='queue_name', exchange='exchange.fanout', routing_key='')
message = "Hello RabbitMQ: "
# 向队列插入数值 routing_key是队列名 body是要插入的内容
for i in range(1, 6, 1):
    # 在发送任务时，用delivery_mode=2来标记消息为持久化存储，1为非持久化，消息持久化的前提是队列持久化
    # expiration,为某条消息的过期时间，单位为ms， 需要为字符串格式
    # priority,消息优先级,值越大，优先级越高，优先被消费。priority生效的条件是queue_declare中需要设置x-max-priority参数，且消费者也需要设置x-max-priority
    channel.basic_publish(exchange='exchange.fanout', routing_key='', body=message+str(i), properties=pika.BasicProperties(
                           expiration=str(i*1000), priority=i))
print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
connection.close()
