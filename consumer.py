import pika,time
import config

user_pwd = pika.PlainCredentials(config.username,config.pwd)
s_conn = pika.BlockingConnection(
    pika.ConnectionParameters('localhost',
                              credentials=user_pwd)
)

chan = s_conn.channel()

chan.queue_declare(queue='task_queue',durable=True)

#定义回调函数，用来接收生产者发送的消息
def callback(ch,method,properties,body):
    print("消费者 recv %s" % body)
    time.sleep(1)
    print("消费者 DOne")
    ch.basic_ack(delivery_tag=method.delivery_tag) #接收到消息后会给rabbitmq发送一个确认,提示其可以删除

chan.basic_qos(prefetch_count=1) #设置公平调度，消费者给mq发送一个消息：在消费者处理完消息之前不要再给消费者发送消息

chan.basic_consume(callback, #调用回调函数，从队列里取消息
                   queue='task_queue', #指定取消息的队列名
                   #no_ack=True  #取完一条消息后，不给生产者发送确认消息，默认是False
                   )

print('消费者 waiting for msg.')

#开始循环取消息
chan.start_consuming()