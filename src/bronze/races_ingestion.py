# Databricks notebook source
%run ../common/ingestion_helpers
# COMMAND ----------
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, IntegerType, DateType

race_schema =  StructType([
    StructField('season', IntegerType()),
    StructField('round', IntegerType()),
    StructField('url', StringType()),
    StructField('raceName', StringType()),
    StructField('date', DateType()),
    StructField('circuitId', StringType())
])
# COMMAND ----------
enriched_races_df = add_metadata(races_df)

display(enriched_races_df)
# COMMAND ----------
races_df = (
    spark.read
        .format('csv')
        .option('header', 'true')
        .schema(race_schema)
        .load('/Volumes/formula1/landing/files/races.csv')
)

display(races_df)
# COMMAND ----------
write_delta_table(enriched_races_df, 'formula1.bronze.races')

display(spark.table('formula1.bronze.races'))