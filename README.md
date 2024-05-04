# Real-Time Insights Engine: Click Attribution and E-commerce Analytics

An end-to-end open-source data stack for crawling and visualizing real estate data, facilitating insights into market trends.

## Preview

![dashboard](/assets//dashboard.png)

## Table of Contents

1. [Introduction](#introduction)
   - [Technologies used](#technologies-used)
2. [Prerequisites](#prerequisites)
3. [Setup and Run](#setup-and-run)
4. [Architecture](#architecture)
   - [Purpose](#purpose)
5. [Data Flow](#data-flow)
6. [Streaming Concept](#streaming-concept)
   - [Time attributes & watermarking](#time-attributes-&-watermarking)
   - [Stream joining](#stream-joining)
7. [Project Overview](#project-overview)
8. [Visualization](#visualization)
9. [Acknowledgements](#acknowledgements)

## Introduction

# Project Name

This project is an end-to-end open-source data stack designed to crawl real estate data and visualize it, aiding in gaining insights into real estate market trends. By leveraging this comprehensive data stack, users can gather and analyze real-time data from various sources within the real estate market. The system provides functionalities for data crawling, processing, storage, and visualization, allowing users to explore and understand market dynamics, property trends, and investment opportunities.

### Technologies Used

Below is a list of technologies used in this project:

| Component | Description |  URL  |
| --------- | ----------- | ----- |
| [Docker](https://www.docker.com/) | Containerization |
| [Spark](https://spark.apache.org/) | Big Data processing framework | http://localhost:8062 \n http://localhost:8063 \n http://localhost:18080 |
| [Jupyter Notebook](https://jupyter.org/) | Interactive computing and data analysis | http://localhost:8888 |
| [Minio](https://min.io/) | Object storage service | http://localhost:9001 |
| [Iceberg](https://iceberg.apache.org/) | Table format for large-scale data |
| [Data Build Tool (DBT)](https://www.getdbt.com/) | Data transformation and modeling |
| [Dagster](https://dagster.io/) | Data orchestrator | http://localhost:3070 |
| [Trino](https://trino.io/) | Distributed SQL query engine |
| [PostgreSQL](https://www.postgresql.org/) | Relational database management system | 

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

1.  Data is generated and sent to Kafka topics.
2.  Flink retrieves this data and performs operations such as enrichment, joining, filtering, recalculating, and aggregation.
3.  Then forward it to the PostgreSQL sink.
4.  Finally, Grafana pulls processed aggregate data for near real-time visualization.

### Purpose:

For each successful attribution, we aim to identify which source the user clicked on, such as TikTok Ads, Google Ads, Facebook posts, etc. This evaluation helps determine the most effective advertising platform in the last hour.

Additionally, we evaluate real-time revenue and profit status, most popular categories, most common failed payment reasons, and customer gender distribution, all within the last hour.

(See details in the [Visualization](#visualization) section below)

## Data Flow

**Source**: Data is generated and sent to two topics: "Clicks" and "Checkouts". Flink listens to these topics and stores the data in source tables.

**Transformation**: After data ingestion, it undergoes a series of transformations including enriching checkout data, filtering out click records older than the last hour, and calculating profit and revenue.

**Processing**: Checkout attribution is performed between the "Checkouts" and "Clicks" topics using a stream-stream join operation. The result is sent to a PostgreSQL sink.

**Sink**: The sink receives the processed data and either persists it or forwards it to Grafana for visualization.

The diagram below illustrates the data flow in Flink.
![data-flow](/assets/data_flow.png)

## Streaming Concept

### Time attributes & watermarking

Understanding time attributes in stream processing is crucial, especially considering the possibility of out-of-order data arrival. There are two main types of [time](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/concepts/time_attributes/) in stream processing:

**Event time**: The time when the event occurred, typically provided by the system generating the data.

**Processing time**: The time when the event is processed by the stream processing system.

![time](/assets/time.png)

As events may arrive late, we need a mechanism to inform Apache Flink how long to wait for an event before considering it for processing. This is where [watermarking](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/dev/datastream/event-time/generating_watermarks/#introduction-to-watermark-strategies) comes into play.

**Watermarking**: A mechanism that instructs the stream processing system to wait for a specified duration before allowing late-arriving events to affect the output. For example, if the watermark is set to 5 minutes, Apache Flink will wait for 5 minutes after the event time before considering any late-arriving events for processing. Any events arriving after this watermark interval will be ignored.

```sql
checkout_timestamp TIMESTAMP(3),
processing_timestamp AS PROCTIME(),
WATERMARK FOR checkout_timestamp AS checkout_timestamp - INTERVAL '15' SECOND
```

In our project, we derive event time from the source data. We define a watermark of 15 seconds on the event time. This means that our clicks and checkouts tables will wait for 15 seconds before being considered complete. Any events arriving later than 15 seconds will not be considered for computation. This ensures that our processing is robust and accurate, even in the presence of late-arriving data.

### Stream joining

In this project, we utilize the **interval join** in Flink, which allows us to join data streams based on a specified time range condition. The interval join is particularly useful when we need to ensure that one stream's time falls within a certain range of time of another stream.

For more details on interval joins or other joins in Flink, refer to the [official documentation](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/operators/joining/#interval-join).

Here's an example of an interval join query used in our project:

```sql
checkouts AS co
    JOIN users FOR SYSTEM_TIME AS OF co.processing_timestamp AS u ON co.user_id = u.user_id
    JOIN products FOR SYSTEM_TIME AS OF co.processing_timestamp AS p ON co.product_id = p.product_id
    LEFT JOIN clicks AS cl ON co.user_id = cl.user_id
        AND co.checkout_timestamp BETWEEN cl.click_timestamp
        AND cl.click_timestamp + INTERVAL '1' HOUR
```

In this query, we match checkouts with clicks based on the condition that the checkout occurred within 1 hour after the click time. This ensures that we only consider clicks that happened within the last hour relative to the checkout time.

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

For visualization using Grafana, access [localhost:3000](http://localhost:3000) (username `admin` and password `admin`).

After accessing Grafana with the provided credentials, choose the **"Ecommerce Monitoring"** dashboard for viewing.

![grafana](/assets/grafana.png)

![dashboard](/assets/dashboard.png)

## Acknowledgements

This project draws inspiration and guidance from the following sources:

- [ngods-stocks](https://github.com/zsvoboda/ngods-stocks) for its valuable insights and inspiration.
- [hcmc-houses-analysis](https://github.com/vietdoo/hcmc-houses-analysis) for generously providing code for data crawling.
