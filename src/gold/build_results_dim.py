# Databricks notebook source
%run ../common/ingestion_helpers
# COMMAND ----------
results_df = (
    spark
        .table(f"{catalog_name}.{silver_schema}.results")
        .withColumn("session_type", F.lit("RACE"))
        .drop("race_name", "race_date", "ingestion_timestamp", "source_file", "result_date")
)
# COMMAND ----------
target_table = f"{catalog_name}.{gold_schema}.fact_session_results"
# COMMAND ----------
%run ../common/environment_config
# COMMAND ----------
from pyspark.sql import functions as F
# COMMAND ----------
fact_session_results_df = (
    results_sprints_df
        .withColumn("is_win", F.col("position") == 1)
        .withColumn("is_podium", F.col("position").between(1, 3))
        .withColumn("has_points", F.col("points") > 0)
        .withColumnRenamed("position", "final_position")
        .withColumnRenamed("position_text", "final_position_text")
)
# COMMAND ----------
results_sprints_df = results_df.unionByName(sprints_df)
# COMMAND ----------
sprints_df = (
    spark
        .table(f"{catalog_name}.{silver_schema}.sprints")
        .withColumn("session_type", F.lit("SPRINT"))
        .drop("race_name", "race_date", "ingestion_timestamp", "source_file", "sprint_date")
)
# COMMAND ----------
write_delta_table(fact_session_results_df, target_table)