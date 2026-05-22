# Databricks notebook source
%run ../common/environment_config
# COMMAND ----------
%run ../common/ingestion_helpers
# COMMAND ----------
enriched_drivers_df = add_metadata(drivers_df)
write_delta_table(enriched_drivers_df, table_name)
display(spark.table(table_name))
# COMMAND ----------
from pyspark.sql.types import StructType, StructField, StringType, DateType

name_schema = StructType([
    StructField('givenName', StringType()),
    StructField('familyName', StringType())
])

drivers_schema = StructType([
    StructField('driverId', StringType()),
    StructField('name', name_schema),
    StructField('dateOfBirth', DateType()),
    StructField('nationality', StringType()),
    StructField('url', StringType())
])
# COMMAND ----------
source_file = f"{landing_folder_path}/drivers.json"
table_name = f"{catalog_name}.{bronze_schema}.drivers"
# COMMAND ----------
drivers_df = (
    spark.read
        .format('json')
        .schema(drivers_schema)
        .option('mode', 'FAILFAST')
        .load(source_file)
)