from pyflink.table import TableEnvironment, EnvironmentSettings
from dotenv import load_dotenv
import os

print('running...')
load_dotenv()

mongodb_conn_string = os.environ.get("mongodb_conn_string")

t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())

t_env.execute_sql(
    f'''
    create table mongodb_source (
        user_id STRING,
        article_id STRING,
        tags ROW<people ARRAY<STRING>, location ROW<landmarks ARRAY<STRING>, localities ARRAY<STRING>, cities ARRAY<STRING>, states ARRAY<STRING>, countries ARRAY<STRING>>, other ARRAY<STRING>>,
        `timestamp` STRING
    )
    with (
        'connector' = 'mongodb',
        'uri' = '{mongodb_conn_string}',
        'database' = 'news_app',
        'collection' = 'user_history'
    )
    '''
)

t_env.execute_sql(
    '''
    select * from mongodb_source
    '''
).print()

