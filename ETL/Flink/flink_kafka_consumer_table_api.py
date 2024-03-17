from pyflink.table import TableEnvironment, EnvironmentSettings
from dotenv import load_dotenv
import os
import json

# json_schema = JsonRowDeserializationSchema.builder().build()
print('running...')
load_dotenv()

cloudkarafka_username = os.environ.get("cloudkarafka_username")
cloudkarafka_password = os.environ.get("cloudkarafka_password")

t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())

# jaas_config = f"""
#     Client {
#         org.apache.kafka.common.security.scram.ScramLoginModule required
#             username="{cloudkarafka_username}"
#             password="{cloudkarafka_password}"
#             mechanism="SCRAM-SHA-512";
#     }
# """

kafka_query = f'''
    create table kafka_source1(
        user_id STRING,
        article_id STRING,
        tags ARRAY<STRING>,
        `timestamp` STRING
    )
    with (
        'connector' = 'kafka',
        'topic' = 'cdzbgqqu-user-history',
        'properties.bootstrap.servers' = 'dory.srvs.cloudkafka.com:9094',
        'properties.group.id' = 'cdzbgqqu-flink-consumer',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json',
        'properties.security.protocol' = 'SASL_SSL',
        'properties.sasl.mechanism' = 'SCRAM-SHA-512',
        'properties.sasl.jaas.config' = 'org.apache.kafka.common.security.scram.ScramLoginModule required username=''{cloudkarafka_username}'' password=''{cloudkarafka_password}'';'
    )
    '''
print(kafka_query)
t_env.execute_sql(kafka_query)

# t_env.execute_sql(
#     f'''
#     create table sink(
#         category VARCHAR,
#         cnt BIGINT
#     )
#     with (
    
#         'connector' = 'filesystem',
#         'format' = 'csv',
#         'path' = '{output_path}'
#     )
#     '''
# )

t_env.execute_sql(
    '''
    select * from kafka_source1
    '''
).print()