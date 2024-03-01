# Import the library
from pykafka import KafkaClient, SslConfig

# Define the Kafka configurations
configs = {
    'hosts': 'SASL_SSL://dory.srvs.cloudkafka.com:9094',
    'security_protocol': 'SASL_SSL',
    'ssl_cafile': 'ETL\Kafka\poc\entrust_2048_ca.cer',
    'sasl_mechanism': 'SCRAM-SHA-512',
    'sasl_username': 'cdzbgqqu',
    'sasl_password': 'qmXtLjGWUsnREpCyCT5ab2wk3r3dfQg6'
}

# sslconfig = SslConfig()

# Create an instance of the KafkaClient class
client = KafkaClient(**configs)

# Get the topic object from the client
topic = client.topics["cdzbgqqu-test"]

# Get a producer object from the topic
producer = topic.get_producer()

# Define a list of messages to send
messages = ["Hello", "World", "From", "Async", "Producer"]

# Send the messages asynchronously
for message in messages:
    producer.produce(message.encode("utf-8"))

# Stop the producer
producer.stop()