from confluent_kafka import Producer
import logging
from datetime import datetime
import json

conf = {
    'bootstrap.servers': 'SASL_SSL://dory.srvs.cloudkafka.com:9094',
    'client.id': 'article-id-producer-test',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': 'cdzbgqqu',
    'sasl.password': 'qmXtLjGWUsnREpCyCT5ab2wk3r3dfQg6',
    'api.version.request': True,
    'acks': 'all',
    'retries': 5
}

producer = Producer(conf)
topic = 'cdzbgqqu-test'

message = {
    'user_id': 'db363fb5-fa2b-4ab4-86d2-09de77a3bb89',
    'article_id': 'e6705e98-ab6d-4d7b-bb92-6f91efdcc60c',
    'timestamp': str(datetime.utcnow().isoformat())
}
# message = {'d': 'd'}
message_json = json.dumps(message)
# message_json = 'F'
print(message_json)

def delivery_report(err, msg):
    if err is not None:
        logging.error('Message delivery failed: {}'.format(err))
    else:
        logging.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

producer.produce(topic, value=message_json, callback=delivery_report)

producer.flush()