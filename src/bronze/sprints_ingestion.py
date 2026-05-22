# Databricks notebook source
%run ../common/ingestion_helpers
# COMMAND ----------
%run ../common/environment_config
# COMMAND ----------
source_files = f"{landing_folder_path}/sprints"
table_name = f"{catalog_name}.{bronze_schema}.sprints"
# COMMAND ----------
sprint_schema = """
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
sprints_df = (
    spark.read
        .format('json')
        .schema(sprint_schema)
        .option('mode', 'FAILFAST')
        .option('multiLine', 'true')
        .load(source_files)
)
# COMMAND ----------
enriched_sprints_df = add_metadata(sprints_df)
write_delta_table(enriched_sprints_df, table_name)
display(spark.table(table_name))