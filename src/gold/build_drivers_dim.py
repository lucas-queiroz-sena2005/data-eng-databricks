# Databricks notebook source
%run ../common/environment_config
# COMMAND ----------
%run ../common/ingestion_helpers
# COMMAND ----------
from pyspark.sql import functions as F
# COMMAND ----------
target_table = f"{catalog_name}.{gold_schema}.dim_drivers"
drivers_df = spark.table(f"{catalog_name}.{silver_schema}.drivers")
ref_nationality_region_df = spark.table(f"{catalog_name}.{gold_schema}.ref_nationality_region")
# COMMAND ----------
dim_drivers_df = (
    drivers_df
        .join(
            ref_nationality_region_df,
            drivers_df.nationality == ref_nationality_region_df.nationality,
            "left"
        )
        .select(
            drivers_df.driver_id,
            drivers_df.given_name.alias("driver_name"),
            drivers_df.date_of_birth,
            drivers_df.nationality,
            ref_nationality_region_df.region.alias("nationality_region")
        )
)
# COMMAND ----------
write_delta_table(dim_drivers_df, target_table)