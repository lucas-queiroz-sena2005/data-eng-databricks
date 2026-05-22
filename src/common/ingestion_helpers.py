# Databricks notebook source
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from typing import Union, List
# COMMAND ----------
def write_delta_table(
    df: DataFrame,
    table_name: str,
    write_mode: str = "overwrite",
    partition_cols: Union[str, List[str], None] = None
) -> None:
    """
    Executes a standardized Delta write operation to the metastore.
    Target table_name must follow the 'catalog.schema.table' format.
    """
    writer = df.write.format("delta").mode(write_mode)
    
    if partition_cols:
        writer = writer.partitionBy(partition_cols)
        
    writer.saveAsTable(table_name)
# COMMAND ----------
def add_metadata(df: DataFrame) -> DataFrame:
    return (
        df
        .withColumn("ingestion_timestamp", F.current_timestamp())
        .withColumn("source_file", F.col("_metadata.file_path"))
    )