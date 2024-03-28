from pyspark.sql import SparkSession
spark = (SparkSession.builder.appName('adls_ops')
    .config("spark.jars.packages", "io.delta:delta-core_2.13:2.4.0")
    # .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    # .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    # .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
    .getOrCreate())

spark.conf.set("fs.azure.account.auth.type.adlsnewsapp.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.adlsnewsapp.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
# spark.conf.set("fs.azure.account.oauth2.client.id.adlsnewsapp.dfs.core.windows.net", "<application-id>")
# spark.conf.set("fs.azure.account.oauth2.client.secret.adlsnewsapp.dfs.core.windows.net",account_key)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.adlsnewsapp.dfs.core.windows.net", "https://adlsnewsapp.dfs.core.windows.net")

adls_path = 'abfss://users-data@adlsnewsapp.dfs.core.windows.net/user-history'

# spark.sql(
#     f'''
#     create table user_history (
#         user_id string,
#         article_id string,
#         tags array<string>,
#         timestamp timestamp
#     )
#     location '{adls_path}'
#     '''
# )


# Create DataFrame representing your data
data = [("John", 30), ("Alice", 25), ("Bob", 35)]
columns = ["name", "age"]
df = spark.createDataFrame(data, columns)

# Write data to Delta table
df.write.format("delta").mode("overwrite").save(adls_path)
