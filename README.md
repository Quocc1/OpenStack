# Real-Time Insights Engine: Click Attribution and E-commerce Analytics

An end-to-end open-source data stack for crawling and visualizing real estate data, facilitating insights into market trends.

## Preview

![dashboard](/assets/dashboard.jpg)

## Table of Contents

1. [Introduction](#introduction)
   - [Technologies used](#technologies-used)
2. [Prerequisites](#prerequisites)
3. [Setup and Run](#setup-and-run)
4. [Architecture](#architecture)
   - [Purpose](#purpose)
5. [Components of the Data Stack](#components-of-the-data-stack)
   - [Data Crawling](#data-crawling): Requests
   - [Data Transformation](#data-transformation): DBT, Apache Spark, Trino
   - [Data Warehousing/Storage](#data-warehousing/storage): MinioS3, Iceberg, PostgreSQL
   - [Data Visualization and Analysis](#data-visualization-and-analysis): Metabase, Jupyter Notebook
   - [Project Orchestration](#project-orchestration): Dagster
6. [Project Overview](#project-overview)
7. [Visualization](#visualization)
8. [Acknowledgements](#acknowledgements)

## Introduction

This project is a holistic, open-source data solution crafted to systematically gather real estate data from Ho Chi Minh City and present it in a visual format, empowering users to glean insights into prevailing market trends. By harnessing this versatile data stack, users can efficiently collect and analyze real-time data from diverse sources within the local real estate market. The system offers robust capabilities for data acquisition, processing, storage, and visualization, enabling users to delve into market dynamics, track property trends, and identify lucrative investment opportunities with ease.

### Technologies Used

Below is a list of technologies used in this project:

| Component | Description |  URL  |
| --------- | ----------- | ----- |
| [Docker](https://www.docker.com/) | Containerization |
| [Spark](https://spark.apache.org/) | Big Data processing framework | http://localhost:8061 `Master` <br> http://localhost:8062 `Worker` <br> http://localhost:18080 `History` |
| [Jupyter Notebook](https://jupyter.org/) | Interactive computing and data analysis | http://localhost:8888 |
| [Minio](https://min.io/) | Object storage service | http://localhost:9001 |
| [Iceberg](https://iceberg.apache.org/) | Table format for large-scale data |
| [Data Build Tool (DBT)](https://www.getdbt.com/) | Data transformation and modeling |
| [Dagster](https://dagster.io/) | Data orchestrator | http://localhost:3070 |
| [Trino](https://trino.io/) | Distributed SQL query engine |
| [PostgreSQL](https://www.postgresql.org/) | OLAP database | 

## Prerequisites

[Docker](https://www.docker.com/) is installed with at least 8GB RAM.

## Setup and Run

1. Pull the project from the repository.

```bash
git clone https://github.com/Quocc1/OpenStack
```

2. Start the Docker engine.

3. CD to the project directory then spin up the docker-compose:

```bash
cd OpenStack
```

4. Then run:

```bash
make run
```

**Note**: Run `make help` or refer to the [Makefile](https://github.com/Quocc1/OpenStack/blob/main/Makefile) for details on commands and execution. Use `make down` to stop the containers.

If you encounter issues running the Makefile on Windows, refer to [this Stack Overflow post](https://stackoverflow.com/questions/2532234/how-to-run-a-makefile-in-windows) for potential solutions.

## Architecture

![architecture](/assets/architecture.png)

The diagram illustrates the conceptual view of the streaming pipeline (from bottom to top).

1. Real estate advertisements are obtained through an API.
2. The advertisements are then stored in Minio S3, leveraging Apache Iceberg for efficient data management.
3. The data undergoes transformation through each [medallion](https://www.databricks.com/glossary/medallion-architecture) stage: bronze, silver, and gold, ensuring quality and consistency.
4. Gold standard data is stored in PostgreSQL for persistent storage.
6. Data is visualized with Metabase for analysis and insights, and Jupyter Notebook is utilized for machine learning.

**The orchestration of these steps is managed by Dagster, while data transformation is handled by DBT.**

### Purpose:

The purpose of this project is to offer a comprehensive end-to-end open-source data stack tailored for analyzing real estate trends in Ho Chi Minh City, Vietnam. It aims to seamlessly acquire, process, store, and visualize real estate data specific to the city. 

By leveraging this data stack, users can gain valuable insights into the dynamic real estate market of Ho Chi Minh City, enabling informed decision-making, trend analysis, and identification of investment opportunities in the region.

(See details in the [Visualization](#visualization) section below)

## Components of the Data Stack

### Data Crawling

### Data Transformation

### Data Warehousing/Storage

### Data Visualization and Analysis

### Project Orchestration


## Project Overview

```
OpenStack/
├── assets/
│   └── pictures
├── code/
│   ├── dbt/
│   │   ├── bronze/
│   │   │   └── model/
│   │   │       └── bronze_raw_data.sql
│   │   ├── silver/
│   │   │   └── model/
│   │   │       └── silver_refined_data.sql
│   │   └── gold/
│   │       └── model/
│   │           └── gold_analytics_data.sql
│   └── real_estate_dagster/
│       └── real_estate_dagster/
│           ├── crawl.py
│           ├── database.py
│           ├── dbt.py
│           ├── end_to_end.py
│           └── ...
├── data/
│   ├── spark/
│   │   └── notebook/Predict_Price_Real_Estate.ipynb
│   └── stage/
│       └── houses.csv
├── docker/
│   ├── metabase/
│   ├── spark_iceberg_dagster_dbt/
│   └── trino/
├── docker-compose.yaml
├── Makefile
└── README.md
```

### Overview

```
real_estate_dagster/
└── real_estate_dagster/
   ├── crawl.py
   ├── database.py
   ├── dbt.py
   ├── end_to_end.py
   └── ...
```

**crawl.py**: A Dagster job responsible for retrieving data via an API and storing it into /var/lib/app/stage/houses.csv.

**database.py**: A Dagster job utilized for initializing databases for Minio, Iceberg, and PostgreSQL.

**dbt.py**: A Dagster job employed for executing DBT models.

**end_to_end.py**: This file combines all Dagster jobs, including database.py, crawl.py, and dbt.py, to orchestrate an end-to-end data 
pipeline.

```
dbt/
├── bronze/
│   └── model/
│       └── bronze_raw_data.sql
├── silver/
│   └── model/
│       └── silver_refined_data.sql
└── gold/
   └── model/
      └── gold_analytics_data.sql
```

**bronze_raw_data.sql**: SQL model defining transformations for raw data in the bronze layer.

**silver_refined_data.sql**: SQL model defining transformations for refined data in the silver layer.

**gold_analytics_data.sql**: SQL model defining transformations for analytics-ready data in the gold layer.

```
data/
├── spark/
│   └── notebook/Predict_Price_Real_Estate.ipynb
└── stage/
   └── houses.csv
```

**Predict_Price_Real_Estate.ipynb**: Jupyter Notebook containing code for predicting real estate prices using Spark.

**houses.csv**: CSV file containing staged real estate data.

## Visualization

For visualization using Metabase, access [localhost:3030](http://localhost:3030) (username `caobinhoh@gmail.com` and password `quoc123`).

After accessing Metabase with the provided credentials, choose the **"HCMC Real Estate Insights"** dashboard for viewing.

![Metabase](/assets/metabase.png)

![dashboard](/assets/dashboard.jpg)

## Acknowledgements

This project draws inspiration and guidance from the following sources:

- [ngods-stocks](https://github.com/zsvoboda/ngods-stocks) for its valuable insights and inspiration.
- [hcmc-houses-analysis](https://github.com/vietdoo/hcmc-houses-analysis) for generously providing code for data crawling.
