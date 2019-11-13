# coding:utf-8
import pika

credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def fib(n):
    """
    斐波那契数列
    :param n:
    :return:
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):  # props 是客户端发过来的消息
    n = int(body)
    print("fib(%s)" % n)
    response = fib(n)
    # 发布消息
    ch.basic_publish(exchange="",
                     routing_key=props.reply_to,  # props.reply_to从客户端取出双方约定好存放返回结果的queue
                     properties=pika.BasicProperties  # 定义一些基本属性
                     (correlation_id=props.correlation_id),  # props.correlation_id 从客户端取出当前请求的ID返回给客户端做验证
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动确认消息被消费


channel.basic_qos(prefetch_count=1)  # 每次最多处理一个客户端发过来的消息
# 消费消息
channel.basic_consume(on_message_callback=on_request,  # 回调函数
                      queue="rpc_queue")

print("Awaiting RPC requests")
channel.start_consuming()
