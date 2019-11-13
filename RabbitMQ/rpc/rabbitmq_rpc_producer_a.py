# coding:utf-8
import pika
import uuid
import time


class FibonacciRpcClient(object):
    def __init__(self):
        # 创建链接
        credentials = pika.PlainCredentials('root', 'rootadmin')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
        self.channel = self.connection.channel()

        # 创建回调队列
        # 回调队列为服务端消费完数据后的返回值存放队列
        # 每个客户端使用随机不同的排他响应信息队列的意义
        # 存在多个客户端时，不能保证响应信息被发布请求的那个客户端消费到，所以为每个客户端创建一个响应队列
        # 这个队列由该客户端来创建并且只能由这个客户端使用并在使用完后删除，所以使用排他队列
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        # 设置回调，只要一收到消息就调用on_response
        self.channel.basic_consume(on_message_callback=self.on_response, auto_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):  # 必须四个参数
        # 响应回调函数
        print "----->", method, props
        # 当服务端返回的id跟当初请求的id一致时，再去读取服务端发送的信息保持数据的一致性
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        # 发送函数
        # 设置响应和回调通道的ID
        self.response = None
        # 唯一id,用来检查是哪个服务发送的数据，便于获取相应的结果
        self.corr_id = str(uuid.uuid4())
        # properties：附加参数
        # reply_to：指定响应结果存储的队列
        # correlation_id：唯一请求id
        self.channel.basic_publish(exchange="", routing_key="rpc_queue",
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(n))
        # 监听回调，当没有数据，就一直循环
        while self.response is None:
            self.connection.process_data_events()  # 非阻塞版的start_consuming()
            print "no msg ......"
            time.sleep(0.5)
        return int(self.response)


if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient()
    print "Requesting fib(8)"
    for i in range(1, 30):
        response = fibonacci_rpc.call(i)
        print "Got %r" % response
