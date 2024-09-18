from aiokafka import AIOKafkaProducer
from datetime import datetime
import asyncio
import ssl
import json
import os


broker = os.environ.get("kafkaBroker")
username = os.environ.get("kafkaUsername")
mechanism = os.environ.get("kafkaSaslMechanism")
password = os.environ.get("kafkaPassword")


config = {
    'bootstrap_servers': broker,
    'client_id': 'article-id-producer',
    'security_protocol': 'SASL_SSL',
    'ssl_context': ssl.create_default_context(),
    'sasl_mechanism': mechanism,
    'sasl_plain_username': username,
    'sasl_plain_password': password
}
print(config)
topic = 'user-history'

# message = {
#     'user_id': 'db363fb5-fa2b-4ab4-86d2-09de77a3bb89',
#     'article_id': 'e6705e98-ab6d-4d7b-bb92-6f91efdcc60c',
#     'timestamp': str(datetime.utcnow().isoformat())+'Z'
# }

async def send_msg(message):
    message_json = json.dumps(message)
    message_bytes = message_json.encode()
    print(type(message_json))
    producer = AIOKafkaProducer(**config)
    await producer.start()
    try:
        asyncio.create_task(producer.send(topic, message_bytes))
    finally:
        await producer.stop()

# asyncio.run(send_msg(message))