# Open Data Stack: Data-driven Real Estate Insights in Ho Chi Minh City

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
   - [Data Warehousing and Storage](#data-warehousing-and-storage): MinioS3, Iceberg, PostgreSQL
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

5. Run end-to-end job in Dagster

Select then end_to_end job

![end_to_end](/assets/end_to_end.png)


copy all the values in [end_to_end.yaml](https://github.com/Quocc1/OpenStack/blob/main/code/real_estate_dagster/real_estate_dagster/end_to_end.yaml) to Launchpad then Launch run

![launchpad](/assets/launchpad.png)

## Architecture

![architecture](/assets/architecture.png)

The diagram illustrates the conceptual view of the data pipeline (from bottom to top).

1. Real estate advertisements are obtained through an API.
2. The advertisements are then stored in Minio S3, leveraging Apache Iceberg for efficient data management.
3. The data undergoes transformation through each [medallion](https://www.databricks.com/glossary/medallion-architecture) stage: `bronze`, `silver`, and `gold`, ensuring quality and consistency.
4. Gold standard data is stored in PostgreSQL for persistent storage.
5. Data is visualized with Metabase for analysis and insights, and Jupyter Notebook is utilized for machine learning.

**The orchestration of these steps is managed by Dagster, while data transformation is handled by DBT.**

### Purpose:

The purpose of this project is to offer a comprehensive end-to-end open-source data stack tailored for analyzing real estate trends in Ho Chi Minh City, Vietnam. It aims to seamlessly acquire, process, store, and visualize real estate data specific to the city. 

By leveraging this data stack, users can gain valuable insights into the dynamic real estate market of Ho Chi Minh City, enabling informed decision-making, trend analysis, and identification of investment opportunities in the region.

(See details in the [Visualization](#visualization) section below)

## Components of the Data Stack

### Data Crawling

Data crawling represents the preliminary phase in which raw data is gathered from diverse sources. Within our infrastructure, we employ the following technology:

   - ![**Requests**](https://pypi.org/project/requests/): This Python library streamlines the process of making HTTP requests, thereby enabling seamless retrieval of data from APIs and web pages.

API Endpoint: [gateway.chotot.com](https://gateway.chotot.com/v1/public/ad-listing?region_v213000&area_v2=13096&cg=1000&o=0&page=1&st=s,k&limit=20&key_param_included=true)

Here is an example response to a request:

![response](/assets/response.png)

### Data Transformation

Data transformation involves processing and refining raw data into a structured format suitable for analysis. We leverage the following technologies for this purpose:

   - **DBT** (Data Build Tool): DBT is utilized for orchestrating the transformation process, enabling the creation of data models and the execution of SQL transformations.

   - **Apache Spark**: As a powerful distributed computing framework, Apache Spark assists in processing large-scale data efficiently, facilitating complex transformations and computations.

   - **Trino** (formerly Presto): Trino serves as a distributed SQL query engine, enabling interactive analysis across various data sources.

Representation of Data Flow:

![dataflow](/assets/dataflow.png)

### Data Warehousing and Storage

Data warehousing and storage form the foundation for storing and managing processed data. Our data stack incorporates the following technologies:

   - **MinioS3**: MinioS3 provides object storage capabilities, offering a scalable and cost-effective solution for storing large volumes of data.
 
   - **Iceberg**: Iceberg is utilized for managing structured data tables in cloud object stores efficiently, providing features like atomic commits and time travel.
 
   - **PostgreSQL**: PostgreSQL serves as our relational database management system, offering robust data storage and querying capabilities.

Connect to PostgreSQL using ![DBeaver](https://dbeaver.io/) (username: `postgres`, password: `postgres`):

![dbeaver](/assets/dbeaver.png)

![postgres_table](/assets/postgres_table.png)

Connect to MinioS3 via [localhost:9001](http://localhost:9001) (username: `admin`, password: `password`):

![minio_data](/assets/minio_data.png)

### Data Visualization and Analysis
Data visualization and analysis is paramount in aiding data exploration and decision-making processes. Our preferred tools for visualization and analysis are:
 
   - **Metabase** (Community Edition): Metabase provides a user-friendly interface, facilitating the creation of interactive dashboards and visualizations. This empowers users to effortlessly derive insights from their data.

   - **Jupyter Notebook**: Jupyter Notebook is another essential tool for data visualization and analysis. It allows users to create and share documents containing live code, equations, visualizations, and narrative text, providing a versatile environment for data exploration and experimentation.

Examples of machine learning in Jupyter Notebook:

![jupyter_notebook](/assets/jupyter_notebook.png)

### Project Orchestration
Project orchestration involves coordinating and managing the various components and processes within our data pipeline. We employ:

   - **Dagster**: Dagster serves as our project orchestration tool, enabling the definition, scheduling, and monitoring of data workflows with a focus on data quality and reliability.

End-to-end pipeline illustration:

![dagster_pipeline](/assets/dagster_pipeline.png)

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
