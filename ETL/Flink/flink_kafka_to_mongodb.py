import logging
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pprint import pprint
from dotenv import load_dotenv
import os
# import json
schema = Types.ROW([
   Types.BASIC_ARRAY(Types.STRING()),
   Types.ROW([
      Types.BASIC_ARRAY(Types.STRING()),
      Types.BASIC_ARRAY(Types.STRING()),
      Types.BASIC_ARRAY(Types.STRING()),
      Types.BASIC_ARRAY(Types.STRING()),
      Types.BASIC_ARRAY(Types.STRING())
   ]),
   Types.BASIC_ARRAY(Types.STRING())
])
print(schema)
json_schema = JsonRowDeserializationSchema.builder().type_info(schema).build()
print(json_schema)
print('running...')
load_dotenv()

cloudkarafka_username = os.environ.get("cloudkarafka_username")
cloudkarafka_password = os.environ.get("cloudkarafka_password")
mongodb_conn_string = os.environ.get("mongodb_conn_string")
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_function(value):
    # Log the received Kafka message
    logging.info(f"Received message: {value}")
    pprint(value)
    return value
    # Continue processing the message
    # ...

# Initialize the StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# Define Kafka consumer properties
kafka_props = {
    'bootstrap.servers': 'dory.srvs.cloudkafka.com:9094',
    'group.id': 'cdzbgqqu-flink-consumer',
    'startup.mode': 'earliest-offset',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.jaas.config': f"'org.apache.kafka.common.security.scram.ScramLoginModule required ' 'username=\"{cloudkarafka_username}\" password=\"{cloudkarafka_password}\";'"
}

# Create a Kafka source

kafka_source = FlinkKafkaConsumer(
    'cdzbgqqu-user-history',
    json_schema,
    kafka_props
)

# Add the source to the environment and apply the process function
data_stream = env.add_source(kafka_source).map(process_function)

data_stream.print()

# Execute the job
env.execute("Kafka Source with Logging")