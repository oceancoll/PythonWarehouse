# coding:utf-8
# ack确认机制
# https://blog.csdn.net/vbirdbest/article/details/78699913
import pika

credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
channel.queue_declare(queue='hello5', durable=True, arguments={'x-max-priority':10})

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # 手动应答模式
    # 确认收到
    channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)

    # 手动拒绝:basic_reject     requeue(重新入队列):Fasle(直接丢弃，相当于告诉队列可以直接删除)，true（重新放入队列）
    # 当重新放入队列,会接收，再放入，陷入死循环
    # channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

    # 重新投递:basic_recover,会把剩余的消息全部放回队列中，
    # true:重新递送的消息不会被当前消费者消费
    # false:重新递送的消息还会被当前消费者消费
    # channel.basic_recover(True)


#   on_message_callback:回掉函数，当接收到该队列的消息时，触发的函数
#   auto_ack:   应答模式，true：自动应答，即消费者获取到消息，该消息就会从队列中删除掉
#               false：手动应答，当从队列中取出消息后，需要程序员手动调用方法应答，如果没有应答，
#               该消息还会再放进队列中，就会出现该消息一直没有被消费掉的现象
channel.basic_consume(queue='hello5', on_message_callback=callback, auto_ack=False)
print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
channel.start_consuming()
