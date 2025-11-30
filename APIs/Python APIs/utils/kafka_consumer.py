from confluent_kafka import Consumer, KafkaException, KafkaError
import ssl



broker = 'pkc-56d1g.eastus.azure.confluent.cloud:9092'
username = 'SMNHPUO67NPWHBFS'
password = 'dPIiGHoZdITcG8ADJxEBQ5skGgH/WyGfZwlPA+9ehSAkd3V6k9n7Kddk46OPIt72'
mechanism = 'PLAIN'

config = {
'bootstrap.servers': broker,
'group.id': 'user-history-dwh-consumer-test2',
'security.protocol': 'SASL_SSL',
# 'context': ssl.create_default_context(),
'auto.offset.reset': 'earliest',
'sasl.mechanism': mechanism,
'sasl.username': username,
'sasl.password': password
}

topic = 'user-history'

def kafka_consumer():
    messages = []
    consumer = Consumer(config)
    consumer.subscribe([topic])

    no_messages_count = 0

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            no_messages_count += 1
        else:
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue  #End of partition, do nothing
                else:
                    raise KafkaException(msg.error())
            
            messages.append(msg.value().decode('utf-8'))

            consumer.commit(msg)
            no_messages_count = 0 #Reset counter on successful message

        if no_messages_count > 2: #No messages for more than a second
            break

    return messages
    
print(kafka_consumer())