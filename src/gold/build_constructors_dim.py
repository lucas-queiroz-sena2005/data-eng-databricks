# Databricks notebook source
%run ../common/environment_config
# COMMAND ----------
%run ../common/ingestion_helpers
# COMMAND ----------
from pyspark.sql import functions as F
# COMMAND ----------
target_table = f"{catalog_name}.{gold_schema}.dim_constructors"
constructors_df = spark.table(f"{catalog_name}.{silver_schema}.constructors")
ref_nationality_region_df = spark.table(f"{catalog_name}.{gold_schema}.ref_nationality_region")
# COMMAND ----------
dim_constructors_df = (
    constructors_df
        .join(
            ref_nationality_region_df,
            constructors_df.nationality == ref_nationality_region_df.nationality,
            "left"
        )
        .select (
            constructors_df.constructor_id,
            constructors_df.constructor_name,
            constructors_df.nationality,
            ref_nationality_region_df.region.alias("nationality_region")
        )
    )
# COMMAND ----------
write_delta_table(dim_constructors_df, target_table)