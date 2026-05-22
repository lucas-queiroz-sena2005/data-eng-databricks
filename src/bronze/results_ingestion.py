# Databricks notebook source
enriched_results_df = add_metadata(results_df)
write_delta_table(enriched_results_df, table_name)
display(spark.table(table_name))
# COMMAND ----------
%run ../common/ingestion_helpers
# COMMAND ----------
from pyspark.sql.types import StructType, StructField, StringType, DateType, IntegerType

result_schema = """
    date DATE,
    raceName STRING,
    round INT,
    season INT,
    url STRING,
    constructorId STRING,
    driverId STRING,
    grid INT,
    laps INT,
    number INT,
    points DOUBLE,
    position INT,
    positionText STRING,
    status STRING
"""
# COMMAND ----------
%run ../common/environment_config
# COMMAND ----------
results_df = (
    spark.read
        .format('json')
        .schema(result_schema)
        .option('mode', 'FAILFAST')
        .load(source_files)
)
# COMMAND ----------
source_files = f"{landing_folder_path}/results"
table_name = f"{catalog_name}.{bronze_schema}.results"