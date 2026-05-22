# Databricks notebook source
%sql

SHOW SCHEMAS;
# COMMAND ----------
%sql
CREATE VOLUME IF NOT EXISTS formula1.landing.files;
# COMMAND ----------
%sql

USE CATALOG formula1;
# COMMAND ----------
%fs ls /Volumes/formula1/landing/files
# COMMAND ----------
%sql

CREATE SCHEMA IF NOT EXISTS formula1.landing;
CREATE SCHEMA IF NOT EXISTS formula1.bronze;
CREATE SCHEMA IF NOT EXISTS formula1.silver;
CREATE SCHEMA IF NOT EXISTS formula1.gold;
# COMMAND ----------
%sql

CREATE CATALOG IF NOT EXISTS formula1
COMMENT 'Main catalog for the formula1 project';