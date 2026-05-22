# Databricks notebook source
dim_races_df = (
    races_df
        .join(
            circuits_df,
            races_df.circuit_id == circuits_df.circuit_id,
            "inner"
        )
        .select (
            races_df.season,
            races_df.round,
            races_df.race_name,
            races_df.race_date,
            circuits_df.circuit_name,
            circuits_df.locality,
            circuits_df.country
        )
    )
# COMMAND ----------
target_table = f"{catalog_name}.{gold_schema}.dim_races"
circuits_df = spark.table(f"{catalog_name}.{silver_schema}.circuits")
races_df = spark.table(f"{catalog_name}.{silver_schema}.races")
# COMMAND ----------
write_delta_table(dim_races_df, target_table)
# COMMAND ----------
from pyspark.sql import functions as F
# COMMAND ----------
%run ../common/ingestion_helpers
# COMMAND ----------
%run ../common/environment_config