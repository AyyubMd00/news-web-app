from pyflink.table import TableEnvironment, EnvironmentSettings
# from pyflink.common import Configuration
from dotenv import load_dotenv
import os
# import json

# json_schema = JsonRowDeserializationSchema.builder().build()
print('running...')
load_dotenv()

cloudkarafka_username = os.environ.get("cloudkarafka_username")
cloudkarafka_password = os.environ.get("cloudkarafka_password")
# account_key = os.environ.get("stg_account_key")

t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())

# jaas_config = f"""
#     Client {
#         org.apache.kafka.common.security.scram.ScramLoginModule required
#             username="{cloudkarafka_username}"
#             password="{cloudkarafka_password}"
#             mechanism="SCRAM-SHA-512";
#     }
# """
# t_env.execute_sql(
#     '''
#     CREATE CATALOG MyCatalog WITH (
#         'type' = 'generic_in_memory',
#         'default-database' = 'my_database'
#     );
#     '''
# )

# t_env.execute_sql("USE CATALOG MyCatalog;")

kafka_query = f'''
    create table kafka_source1(
        user_id STRING,
        article_id STRING,
        tags ROW<people ARRAY<STRING>, location ROW<landmarks ARRAY<STRING>, localities ARRAY<STRING>, cities ARRAY<STRING>, states ARRAY<STRING>, countries ARRAY<STRING>>, other ARRAY<STRING>>,
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

t_env.execute_sql(
    '''
    create table mongodb_sink (
        user_id STRING,
        article_id STRING,
        tags ROW<people ARRAY<STRING>, location ROW<landmarks ARRAY<STRING>, localities ARRAY<STRING>, cities ARRAY<STRING>, states ARRAY<STRING>, countries ARRAY<STRING>>, other ARRAY<STRING>>,
        `timestamp` STRING
    )
    with (
        'connector' = 'mongodb',
        'uri' = 'mongodb+srv://AyyubMd00:ayyUB2000@cluster0.mozxcn1.mongodb.net/',
        'database' = 'news_app',
        'collection' = 'user_history'
    )
    '''
)

t_env.execute_sql(
    '''
    insert into mongodb_sink
    select * from kafka_source1
    '''
).wait()