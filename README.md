# Formula 1 Data Engineering Project

A Databricks-based data pipeline for processing and analyzing historical Formula 1 data.

## Project Goal
To transform raw F1 data (circuits, drivers, results, etc.) into a structured analytical format suitable for BI reporting and performance analysis.

## Architecture
The project follows the **Medallion Architecture**:
*   **Bronze**: Raw data ingestion into Delta tables.
*   **Silver**: Data cleaning, deduplication, and standardization.
*   **Gold**: Business-level aggregates and dimensional modeling (Star Schema).

## Contents
*   `src/`: Cleaned Python and SQL source code organized by layer.
*   `Formula-1.dbc`: Complete Databricks archive for easy import.
