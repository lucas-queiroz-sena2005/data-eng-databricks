# Databricks notebook source
circuits_df = (
    spark.read
        .format('csv')
        .option('header', 'true')
#        .option('inferSchema', 'true')
        .schema(circuit_schema)
        .load('/Volumes/formula1/landing/files/circuits.csv')
)

display(circuits_df)
# COMMAND ----------
write_delta_table(enriched_circuits_df, 'formula1.bronze.circuits')
display(spark.table('formula1.bronze.circuits'))
# COMMAND ----------
%run ../common/ingestion_helpers
# COMMAND ----------
from pyspark.sql.types import StructType, StructField, DoubleType, StringType

circuit_schema = StructType([
    StructField('circuitId', StringType()),
    StructField('url', StringType()),
    StructField('circuitName', StringType()),
    StructField('lat', DoubleType()),
    StructField('long', DoubleType()),
    StructField('locality', StringType()),
    StructField('country', StringType())
])
# COMMAND ----------
enriched_circuits_df = add_metadata(circuits_df)

display(enriched_circuits_df)