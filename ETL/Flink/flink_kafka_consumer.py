from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from dotenv import load_dotenv
import os
import json

# json_schema = JsonRowDeserializationSchema.builder().build()
print('running...')
load_dotenv()

cloudkarafka_username = os.environ.get("cloudkarafka_username")
cloudkarafka_password = os.environ.get("cloudkarafka_password")

env = StreamExecutionEnvironment.get_execution_environment()
print(cloudkarafka_username, cloudkarafka_password)
# Kafka configurations
kafka_properties = {
    "bootstrap.servers": "dory.srvs.cloudkafka.com:9094",
    "group.id": "flink_consumer",
    "security.protocol": "SASL_SSL",  # or "SASL_SSL" for SSL encryption
    "sasl.mechanism": "SCRAM-SHA-512",  # Use SCRAM-SHA-512 for SHA-512 authentication
    "sasl.jaas.config": (
        "org.apache.kafka.common.security.scram.ScramLoginModule required "
        f"username={cloudkarafka_username} password={cloudkarafka_password};"
    ),
}
topic = 'cdzbgqqu-user-history'

# Flink Kafka Consumer
kafka_source = FlinkKafkaConsumer(
    topic,  # replace with your Kafka topic
    SimpleStringSchema(),  # replace with the appropriate deserialization schema
    properties=kafka_properties
)

# Add the Kafka source to the Flink DataStream
data_stream = env.add_source(kafka_source)

env.add_source(kafka_source).map(lambda x: json.loads(x)).print()
# Additional processing or transformations can be applied to the data_stream here

# Execute the Flink job
env.execute("FlinkKafkaProducer")
