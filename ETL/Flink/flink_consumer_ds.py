from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema

from dotenv import load_dotenv
import os

load_dotenv()

cloudkarafka_username = os.environ.get("cloudkarafka_username")
cloudkarafka_password = os.environ.get("cloudkarafka_password")

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

kafka_props = {
    'bootstrap.servers': 'dory.srvs.cloudkafka.com:9094',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.jaas.config': f'org.apache.kafka.common.security.scram.ScramLoginModule required username=''cdzbgqqu'' password=''qmXtLjGWUsnREpCyCT5ab2wk3r3dfQg6'';',
    'group.id': 'cdzbgqqu-article-id-consumer'
}
print(kafka_props)
consumer = FlinkKafkaConsumer(
    'cdzbgqqu-user-history',  # source topic
    SimpleStringSchema(),  # message deserialization schema
    properties=kafka_props
)
source_stream = env.add_source(consumer)

# sink = FlinkKafkaProducer(
#     'test',  # target topic
#     serialization_schema=SimpleStringSchema(),
#     producer_config=kafka_props
#     # flink_partitioner='fixed'
# )
# source_stream.add_sink(sink)

source_stream.print()

env.execute("KafkaConsumerJob")