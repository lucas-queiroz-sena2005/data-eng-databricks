# Databricks notebook source
%run ../common/ingestion_helpers
# COMMAND ----------
%run ../common/environment_config
# COMMAND ----------
source_files = f"{landing_folder_path}/constructors.json"
table_name = f"{catalog_name}.{bronze_schema}.constructors"
# COMMAND ----------
sprint_schema = """
    constructorId STRING,
    name STRING,
    nationality STRING,
    url STRING
"""
# COMMAND ----------
constructors_df = (
    spark.read
        .format('json')
        .schema(sprint_schema)
        .option('mode', 'FAILFAST')
        .option('multiLine', 'true')
        .load(source_files)
)
# COMMAND ----------
enriched_constructors_df = add_metadata(constructors_df)
write_delta_table(enriched_constructors_df, table_name)
display(spark.table(table_name))