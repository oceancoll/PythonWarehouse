# coding:utf-8
# 普通模式的生产者
import pika

credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
channel.queue_declare(queue='hello5', durable=True, arguments={'x-max-priority':10})

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

#   on_message_callback:回掉函数，当接收到该队列的消息时，触发的函数
#   auto_ack:   应答模式，true：自动应答，即消费者获取到消息，该消息就会从队列中删除掉
#               false：手动应答，当从队列中取出消息后，需要程序员手动调用方法应答，如果没有应答，
#               该消息还会再放进队列中，就会出现该消息一直没有被消费掉的现象
channel.basic_consume(queue='hello5', on_message_callback=callback, auto_ack=True)
print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
channel.start_consuming()
