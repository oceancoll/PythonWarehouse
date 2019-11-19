# coding:utf-8
# 封装了生产者
# 正常单队列模式中，瓶颈点经常出现在queue中，因此优化点是使用多queue来接收消息
# 实现方式底层使用direct类型的exchange，使用多routing_key对应多个queue，使queue不成为性能瓶颈
# 而在实际消息产生层，不用管具体的发送逻辑
import pika
import random

class RmqEncapsulation(object):
    def __init__(self, subdivsionNum):
        self.host = "106.12.200.182"
        self.port = 5672
        self.vhost = "test2_vhost"
        self.username = "root"
        self.password = "rootadmin"
        self.subdivsionNum = subdivsionNum
        self.connection = None

    def newConnection(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port, self.vhost, credentials))

    def getConnection(self):
        if not self.connection:
            self.newConnection()
        return self.connection

    def closeConnection(self):
        if not self.connection:
            self.connection.close()

    def exchangeDeclare(self, channel, exchange, type, durable, autoDelete, arguments):
        channel.exchange_declare(exchange=exchange, exchange_type=type, durable=durable, auto_delete=autoDelete
                                 , arguments=arguments)

    def queueDeclare(self, channel, queue, durable, exclusive, autoDelete, arguments):
        for i in range(self.subdivsionNum):
            queueName = queue + "_" + str(i)
            channel.queue_declare(queue=queueName, durable=durable, exclusive=exclusive, auto_delete=autoDelete, arguments=arguments)

    def queueBind(self, channel, queue, exchange, routingKey, arguments):
        for i in range(self.subdivsionNum):
            rkName = routingKey + "_" + str(i)
            queueName = queue + "_" + str(i)
            channel.queue_bind(queue=queueName, exchange=exchange, routing_key=rkName, arguments=arguments)

    def basicPublish(self, channel, exchange, routingKey, mandatory, props, body):
        index = random.randint(0, self.subdivsionNum-1)
        rkName = routingKey + "_" + str(index)
        channel.basic_publish(exchange=exchange, routing_key=rkName, mandatory=mandatory, properties=props, body=str(body))


rmqEncapsulation = RmqEncapsulation(4)
connection = rmqEncapsulation.getConnection()
channel = connection.channel()
EXCHANGE = "testexchange"
EXCHANGE_TYPE = "direct"
QUEUE = "testqueue"
ROUTINGKEY = "rk"
rmqEncapsulation.exchangeDeclare(channel, EXCHANGE, EXCHANGE_TYPE, True, False, None)
rmqEncapsulation.queueDeclare(channel, QUEUE, True, False, False, None)
rmqEncapsulation.queueBind(channel, QUEUE, EXCHANGE, ROUTINGKEY, None)
for i in range(100000):
    rmqEncapsulation.basicPublish(channel, EXCHANGE, ROUTINGKEY, False, False, i)
rmqEncapsulation.closeConnection()
