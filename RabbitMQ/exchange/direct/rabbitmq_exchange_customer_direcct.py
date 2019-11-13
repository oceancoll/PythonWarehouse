# coding:utf-8
# exchange下的direct模式消费者
# 可以启动任意多个消费者，当生产者启动后，不同的消费者根据routing_key接收不同的消息
import pika

credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
channel = connection.channel()
# 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
channel.exchange_declare(exchange='python-test2', exchange_type='direct')
# 创建临时队列，consumer关闭后，队列自动删除
# 使用空白字符会使用随机的队列名字，类似于"amq.gen-Q48wnVe5JFf7BGlgeTWPWA"
# exclusive=True属性，当连接断开时，队列应该自动删除
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
# 绑定队列和Exchange。
# 根据绑定的exchange时，当所在的routing_key有消息时，则消费该消息
# 使得队列能够接收到来自Exchange的消息，所以需要把它们两者绑定起来
# 如果没有队列绑定到Exchange，生产者发送到该Exchange的消息会被丢弃
channel.queue_bind(exchange='python-test2', queue=queue_name, routing_key="OrderId")
channel.queue_bind(exchange='python-test2', queue=queue_name, routing_key="OrderId1")
print(' [*] Waiting for logs. To exit press CTRL+C')


# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    "回调函数"
    print("[X] {0}".format(body))


# auto_ack:自动确认。消费者只关心最新的消息，不需要关心已经丢失的旧消息。等效于no_ack=True
channel.basic_consume(queue_name, callback, auto_ack=True)
channel.start_consuming()
