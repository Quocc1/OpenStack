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
   - [Data Crawling](#data-crawling): Requests, API Gateway
   - [Data Transformation](#data-transformation): DBT, Apache Spark, Trino
   - [Data Warehousing/Storage](#data-warehousing/storage): MinioS3, Iceberg, PostgreSQL
   - [Data Visualization](#data-visualization): Metabase (Community Edition)
   - [Project Orchestration](#project-orcstration): Dagster
7. [Project Overview](#project-overview)
8. [Visualization](#visualization)
9. [Acknowledgements](#acknowledgements)

## Introduction

This project is a holistic, open-source data solution crafted to systematically gather real estate data from Ho Chi Minh City and present it in a visual format, empowering users to glean insights into prevailing market trends. By harnessing this versatile data stack, users can efficiently collect and analyze real-time data from diverse sources within the local real estate market. The system offers robust capabilities for data acquisition, processing, storage, and visualization, enabling users to delve into market dynamics, track property trends, and identify lucrative investment opportunities with ease.

### Technologies Used

Below is a list of technologies used in this project:

| Component | Description |  URL  |
| --------- | ----------- | ----- |
| [Docker](https://www.docker.com/) | Containerization |
| [Spark](https://spark.apache.org/) | Big Data processing framework | http://localhost:8061 `Master` http://localhost:8062 `Worker` http://localhost:18080 `History` |
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

1. Real estate advertisements are obtained through an API Gateway.
2. The advertisements are then stored in Minio S3, leveraging Apache Iceberg for efficient data management.
3. The data undergoes transformation through each [medallion](https://www.databricks.com/glossary/medallion-architecture) stage: bronze, silver, and gold, ensuring quality and consistency.
4. Gold standard data is stored in PostgreSQL for persistent storage.
5. The data is visualized using Metabase for analysis and insights.

The orchestration of these steps is managed by Dagster, while data transformation is handled by DBT.

### Purpose:

The purpose of this project is to offer a comprehensive end-to-end open-source data stack tailored for analyzing real estate trends in Ho Chi Minh City, Vietnam. It aims to seamlessly acquire, process, store, and visualize real estate data specific to the city. 

By leveraging this data stack, users can gain valuable insights into the dynamic real estate market of Ho Chi Minh City, enabling informed decision-making, trend analysis, and identification of investment opportunities in the region.

(See details in the [Visualization](#visualization) section below)

## Project Overview

```
Stream_Processing
├── assets/
│   └── pictures
├── code/
│   ├── generate_data/
│   │   └── gen_data.py
│   ├── process/
│   │   └── insert_into_sink.sql
│   ├── sink/
│   │   └── checkout_attribution.sql
│   ├── source/
│   │   ├── checkouts.sql
│   │   ├── clicks.sql
│   │   ├── products.sql
│   │   └── users.sql
│   └── main.py
├── container/
│   ├── flink/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── generate_data/
│       ├── Dockerfile
│       └── requirements.txt
├── data/
│   ├── Products.csv
│   └── Users.csv
├── grafana/
│   └── provisioning/
│       ├── dashboards/
│       │   ├── dashboard.json
│       │   └── dashboard.yml
│       └── datasources/
│           └── postgres.yml
├── postgres/
│   └── init.sql
├── .gitignore
├── docker-compose.yaml
├── Makefile
└── README.md
```

### Overview

```
├── generate_data/
│   └── gen_data.py
```

**gen_data.py**: Generates and populates data into Kafka topics "clicks" and "checkouts".

```
├── source/
│   ├── checkouts.sql
│   ├── clicks.sql
│   ├── products.sql
│   └── users.sql
```

**checkouts.sql:** Defines source tables to retrieve data from Kafka checkouts topics, watermarks are set to "15 seconds".

**chicks.sql:** Defines source tables to retrieve data from Kafka clicks topics, watermarks are set to "15 seconds".

**products.sql** and **users.sql**: Define [temporary tables](https://www.freecodecamp.org/news/sql-temp-table-how-to-create-a-temporary-sql-table/#:~:text=A%20temporary%20SQL%20table%2C%20also,require%20a%20permanent%20storage%20solution.) for streaming joins.

```
├── sink/
│   └── checkout_attribution.sql
```

**checkout_attribution.sql**: Define a sink table that stores the final result from joining the stream

```
├── process/
│   └── insert_into_sink.sql
```

**insert_into_sink.sql**:

- Defines SQL script for processing data by joining stream data from Kafka topics "clicks" and "checkouts" within the last 1 hour.
- Finally, results are written into the PostgreSQL.

```
│   └── main.py
```

**main.py**: Creates sources, sink, and executes data processing.

## Visualization

For visualization using Metabase, access [localhost:3030](http://localhost:3030) (username `caobinhoh@gmail.com` and password `quoc123`).

After accessing Metabase with the provided credentials, choose the **"HCMC Real Estate Insights"** dashboard for viewing.

![Metabase](/assets/metabase.png)

![dashboard](/assets/dashboard.jpg)

## Acknowledgements

This project draws inspiration and guidance from the following sources:

- [ngods-stocks](https://github.com/zsvoboda/ngods-stocks) for its valuable insights and inspiration.
- [hcmc-houses-analysis](https://github.com/vietdoo/hcmc-houses-analysis) for generously providing code for data crawling.
