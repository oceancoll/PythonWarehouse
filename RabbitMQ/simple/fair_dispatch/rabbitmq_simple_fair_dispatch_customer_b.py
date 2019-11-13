# coding:utf-8
# 公平调度模式

# 轮训分发
# 正常情况下，使用轮训分发的规则。遍历消费者，逐个发送消息到每个消费者，不考虑每个任务的耗时时长
# 且是提前一次性分配，并非一个一个分配，平均每个消费者得到相同数量的消息
# 假设有2个消费者，一个处理的速度快，一个处理的速度慢，结果也是一个处理的是偶数类，一个处理的是奇数类
# 而非是等处理完了再进行分配

# 公平调度模式
# 公平调度模式是根据每个任务处理速度的不同进行合理的分配，处理快的处理的多
# 通过channel.basic_qos(prefetch_count=1)进行控制
# 该模式下，ack_auto自动应答模式应该处于关闭状态，改为手动应答模式：channel.basic_ack(delivery_tag=method.delivery_tag)
# no_ack=False的目的：当工作者挂掉后，防止任务丢失



import pika
import time
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
# 声明消息队列，消息将在这个队列中进行传递。如果将消息发送到不存在的队列，rabbitmq将会自动清除这些消息。如果队列不存在，则创建
channel.queue_declare(queue='hello3')
channel.basic_qos(prefetch_count=1)
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(5)
    channel.basic_ack(delivery_tag=method.delivery_tag)
# exchange -- 它使我们能够确切地指定消息应该到哪个队列去。
# 向队列插入数值 routing_key是队列名 body是要插入的内容

channel.basic_consume(queue='hello3',on_message_callback=callback, auto_ack=False)
print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
channel.start_consuming()