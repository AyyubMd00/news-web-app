from aiokafka import AIOKafkaProducer
from datetime import datetime, UTC
import asyncio
import ssl
import json
import os


broker = os.environ.get("kafkaBroker")
username = os.environ.get("kafkaUsername")
mechanism = os.environ.get("kafkaSaslMechanism")
password = os.environ.get("kafkaPassword")

broker = 'pkc-56d1g.eastus.azure.confluent.cloud:9092'
username = 'SMNHPUO67NPWHBFS'
password = 'dPIiGHoZdITcG8ADJxEBQ5skGgH/WyGfZwlPA+9ehSAkd3V6k9n7Kddk46OPIt72'
mechanism = 'PLAIN'


config = {
    'bootstrap_servers': broker,
    'client_id': 'article-id-producer',
    'security_protocol': 'SASL_SSL',
    'ssl_context': ssl.create_default_context(),
    'sasl_mechanism': mechanism,
    'sasl_plain_username': username,
    'sasl_plain_password': password
}
topic = 'user-history'

# message = {
#     'user_id': 'db363fb5-fa2b-4ab4-86d2-09de77a3bb89',
#     'article_id': 'e6705e98-ab6d-4d7b-bb92-6f91efdcc60c',
#     'timestamp': str(datetime.now(UTC))[:-6]+'Z'
# }

async def send_msg(message):
    message_json = json.dumps(message)
    message_bytes = message_json.encode()
    producer = AIOKafkaProducer(**config)
    await producer.start()
    try:
        asyncio.create_task(producer.send(topic, message_bytes))
    finally:
        await producer.stop()

# asyncio.run(send_msg(message))