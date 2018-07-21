import pika
import sys
import config

user_pwd = pika.PlainCredentials(config.username,config.pwd) #

#创建链接
s_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost',credentials=user_pwd))

#创建一个频道
chan = s_conn.channel()

#声明一个队列,设置队列持久化
chan.queue_declare(queue='task_queue',durable=True)

chan.basic_publish(exchange='',#交换机
                   routing_key='task_queue',#路由键，写明将消息发往哪个队列，本例是将消息发往队列hello)
                   body='hello world',#生产者要发送的消息
                   properties=pika.BasicProperties(delivery_mode=2,) #设置持久化
                   )
print("生产者 send helloworld")

#生产者发送完消息后，关闭链接
#s_conn.close()