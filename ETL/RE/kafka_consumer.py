from confluent_kafka import Consumer, KafkaException
import os
import json
from process_hist import process_hist


cloudkarafka_username = os.environ.get("cloudkarafka_username")
cloudkarafka_password = os.environ.get("cloudkarafka_password")

config = {
    'bootstrap.servers': 'dory.srvs.cloudkafka.com:9094',
    'group.id': 'cdzbgqqu-article-id-consumer-test',
    'security.protocol': 'SASL_SSL',
    # 'ssl.context': ssl.create_default_context(),
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': 'cdzbgqqu',
    'sasl.password': 'qmXtLjGWUsnREpCyCT5ab2wk3r3dfQg6',
    'auto.offset.reset': 'earliest',  # or 'latest'
}

topic = 'cdzbgqqu-user-history'

# Create consumer object
consumer = Consumer(config)

# def on_assign(consumer, partitions):
#     """ Callback for partition assignment """
#     for partition in partitions:
#         consumer.seek_beginning(partition)
#         print(f"Consumer assigned to partition {partition.topic}:{partition.id}")

def consume_messages(consumer):
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Timeout in seconds
            if msg is None:
                continue
            elif msg.error():
                raise KafkaException(f"Error consuming: {msg.error()}")
            else:
                hist_str = msg.value().decode('utf-8')
                hist = json.loads(hist_str)
                process_hist(hist)
                # load_data(hist, hist['user_id'])
                print(f"Received message: {hist}")
                consumer.commit()  # Commit offset
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

consumer.subscribe([topic])
consume_messages(consumer)