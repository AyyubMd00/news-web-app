from confluent_kafka import Consumer, KafkaError
# from datetime import datetime
# import json

conf = {
    'bootstrap.servers': 'SASL_SSL://dory.srvs.cloudkafka.com:9094',
    'client.id': 'article-id-producer-test',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': 'cdzbgqqu',
    'sasl.password': 'qmXtLjGWUsnREpCyCT5ab2wk3r3dfQg6',
    'group.id': 'cdzbgqqu-article-id-consumer',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

consumer = Consumer(conf)
topic = 'cdzbgqqu-test'

consumer.subscribe([topic])

arr = []

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages, timeout set to 1.0 seconds

        if msg is None:
            # print(None)
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event, not an error
                continue
            else:
                print(msg.error())
                break

        # Print the received message value
        # print('Received message: {}'.format(msg.value().decode('utf-8')))
        arr.append(msg.value().decode('utf-8'))
        print(arr)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()