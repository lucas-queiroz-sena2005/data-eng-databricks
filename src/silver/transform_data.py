# Databricks notebook source
transformation_configs = {
  "circuits": {
    "select_cols": ["circuitId", "circuitName", "lat", "long", "locality", "country", "ingestion_timestamp", "source_file"],
    "renames": {"circuitId": "circuit_id", "circuitName": "circuit_name", "lat": "latitude", "long": "longitude"},
    "initcap_cols": ["circuit_name", "locality"],
    "dedup_cols": ["circuit_id"]
  },
  "races": {
    "select_cols": ["season", "round", "raceName", "date", "circuitId", "ingestion_timestamp", "source_file"],
    "renames": {"circuitId": "circuit_id", "raceName": "race_name", "date": "race_date"},
    "initcap_cols": ["race_name"],
    "dedup_cols": ["season", "round"]
  },
  "drivers": {
    "select_cols": ["driverId", "name.givenName", "name.familyName", "dateOfBirth", "nationality", "ingestion_timestamp", "source_file"],
    "renames": {"driverId": "driver_id", "name.givenName": "given_name", "name.familyName": "family_name", "dateOfBirth": "date_of_birth"},
    "initcap_cols": ["given_name", "family_name", "nationality"],
    "dedup_cols": ["driver_id"]
  },
  "sprints": {
    "select_cols": ["season", "round", "raceName", "date", "driverId", "constructorId", "grid", "laps", "number", "points", "position", "positionText", "status", "ingestion_timestamp", "source_file"],
    "renames": {"raceName": "race_name", "driverId": "driver_id", "constructorId": "constructor_id", "positionText": "position_text", "date": "sprint_date"},
    "initcap_cols": ["race_name", "status"],
    "dedup_cols": ["season", "round", "driver_id"]
  },
  "constructors": {
    "select_cols": ["constructorId", "name", "nationality", "ingestion_timestamp", "source_file"],
    "renames": {"constructorId": "constructor_id", "name": "constructor_name"},
    "initcap_cols": ["constructor_name", "nationality"],
    "dedup_cols": ["constructor_id"]
  },
  "results": {
    "select_cols": ["season", "round", "raceName", "date", "driverId", "constructorId", "grid", "laps", "number", "points", "position", "positionText", "status", "ingestion_timestamp", "source_file"],
    "renames": {"raceName": "race_name", "driverId": "driver_id", "constructorId": "constructor_id", "positionText": "position_text", "date": "result_date"},
    "initcap_cols": ["race_name", "status"],
    "dedup_cols": ["season", "round", "driver_id"]
  }
}
# COMMAND ----------
%run ../common/environment_config
# COMMAND ----------
from pyspark.sql import functions as F
# COMMAND ----------
dbutils.widgets.dropdown("table_name", "circuits", ["circuits", "races", "drivers", "sprints", "constructors", "results"])
table_name = dbutils.widgets.get("table_name")

if table_name not in transformation_configs:
    raise ValueError(f"Table '{table_name}' not defined in transformation_configs.")

config = transformation_configs[table_name]
bronze_table = f"{catalog_name}.{bronze_schema}.{table_name}"
silver_table = f"{catalog_name}.{silver_schema}.{table_name}"
# COMMAND ----------
(
    df.write
      .format("delta")
      .mode("overwrite")
      .saveAsTable(silver_table)
)
# COMMAND ----------
display(spark.table(silver_table))
# COMMAND ----------
df = spark.table(bronze_table)

select_exprs = [
    F.col(c).alias(config.get("renames", {}).get(c, c)) 
    for c in config.get("select_cols", [])
]
df = df.select(*select_exprs)

if "initcap_cols" in config:
    for col_name in config["initcap_cols"]:
        df = df.withColumn(col_name, F.initcap(F.col(col_name)))

if "dedup_cols" in config:
    df = df.dropDuplicates(config["dedup_cols"])