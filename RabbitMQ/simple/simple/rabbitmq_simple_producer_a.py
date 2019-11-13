# coding:utf-8
# 普通模式的生产者
import pika
credentials = pika.PlainCredentials('root', 'rootadmin')
connection = pika.BlockingConnection(pika.ConnectionParameters('106.12.200.182', 5672, '/', credentials))
# 创建频道
channel = connection.channel()
# queue_declare用于绑定队列，如果不存在则创建。
# 如果队列不存在，则在basic_publish时无法发送，消息会丢失，如果queue已经存在，实际上不需要绑定queue.但为了兼容，还是绑定为好
# queue:队列名称
# passive:只是用于检查队列是否存在，存在时返回true,不存在时不会创建返回失败
# durable：是否持久化
# exclusive：排他锁，只有创建它的连接有权访问。用于区分的是连接，同一个连接不同通道可以同时访问某一个排他队列
#            连接断开后，排他队列将自动删除。这种队列适用于一个队列仅对应一个客户端收发消息的场景。
#            关键的提示信息为“cannot obtain exclusive access to locked queue”，无法获取加锁队列的访问权限，即该队列对于其他连接是无权访问的。
# auto_delete：当队列的最后一个消费者断开时，该队列会被自动删除
# channel.queue_declare(queue='hello', passive=False, durable=False, exclusive=False, auto_delete=False)
# arguments中，
#       x-message-ttl:整个队列中消息过期时间，单位为ms.
#       x-expires:当多长时间没有消费者访问该队列的时候，该队列会自动删除
#       x-max-length:队列的最大长度,当超过4条消息，前面的消息将被删除，给后面的消息腾位
#       x-max-length-bytes:指定队列存储消息的占用空间大小，当达到最大值是会删除之前的数据腾出空间
#       x-max-priority:设置消息的优先级，优先级值越大，越被提前消费
# channel.queue_declare(queue='hello4', durable=True,
#   arguments={'x-message-ttl': 10000, 'x-expires': 10000, 'x-max-length': 4, 'x-max-length-bytes':1024,
#   'x-max-priority':10})
channel.queue_declare(queue='hello', durable=True)
# 向队列插入数值 routing_key是队列名 body是要插入的内容
for i in range(10):
    # 在发送任务时，用delivery_mode=2来标记消息为持久化存储，1为非持久化，消息持久化的前提是队列持久化
    # expiration,为某条消息的过期时间，单位为ms， 需要为字符串格式
    # priority,消息优先级,值越大，优先级越高，优先被消费。priority生效的条件是queue_declare中需要设置x-max-priority参数，且消费者也需要设置x-max-priority

    # properties参数:
    #   content_type ： 消息内容的类型
    #   content_encoding： 消息内容的编码格式
    #   priority： 消息的优先级
    #   correlation_id：关联id
    #   reply_to: 用于指定回复的队列的名称
    #   expiration： 消息的失效时间
    #   message_id： 消息id
    #   timestamp：消息的时间戳
    #   type： 类型
    #   user_id: 用户id
    #   app_id： 应用程序id
    #   cluster_id: 集群id


    # basic_publish 中 mandatory
    # mandatory：告诉服务器至少将该消息route到一个队列中，否则将消息返还给生产者
    # immediate：告诉服务器如果该消息关联的queue上有消费者，则马上将消息投递给它，如果所有queue都没有消费者，直接把消息返还给生产者，不用将消息入队列等待消费者了
    # channel.basic_publish(exchange='', routing_key='', body=str(i), mandatory=True, immediate=True)

    channel.basic_publish(exchange='', routing_key='hello', body=str(i), properties=pika.BasicProperties(
                           delivery_mode=2, expiration='1000', priority=i))
print("开始队列")
# 缓冲区已经flush而且消息已经确认发送到了RabbitMQ中，关闭链接
connection.close()
