# Docker data stack

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Run](#run)
- [Jupyter](#jupyter)
- [Trino](#trino)
- [Spark](#spark)
  - [Run spark containers](#run-spark-containers)
  - [Run spark jobs](#run-spark-jobs)
- [Thrift](#thrift)
- [ScyllaDB](#scylladb)
  - [Connect to cqlsh](#connect-to-cqlsh)
  - [Create keyspace](#create-keyspace)
  - [Use keyspace and create table](#use-keyspace-and-create-table)
  - [Insert data](#insert-data)
- [Kafka](#kafka)
  - [Create topic](#create-topic)
  - [Kafka producer](#kafka-producer)
  - [Kafka consumer](#kafka-consumer)
- [Airflow](#airflow)
  - [Slack integration](#slack-integration)
- [Mongo](#mongo)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Run

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Create `.env` file in the repo root by copying `.env.template`
3. Fill in the desired `POSTGRES_PASSWORD` value in the `.env` file
4. Build containers:

```bash
docker compose up -d --build
```

## Jupyter

Check out the `jupyterlab` container logs and click on the link that looks like `http://127.0.0.1:8089/lab?token=...`

## Trino

```bash
docker exec -it trino trino
```

```bash
SHOW SCHEMAS FROM db;
```

```bash
USE db.public;
```

```bash
SHOW TABLES FROM public;
```

## Spark

### Run spark containers

```bash
docker compose --profile spark up -d
```

### Run spark jobs

```bash
docker exec -it spark-master /bin/bash
```

```bash
cd /opt/spark/bin
./spark-submit --master spark://0.0.0.0:7077 \
  --name spark-pi \
  --class org.apache.spark.examples.SparkPi  \
  local:///opt/spark/examples/jars/spark-examples_2.12-3.5.1.jar 100
```

## Thrift

```bash
docker exec -it spark-master /bin/bash
```

```bash
./bin/beeline
```

```bash
!connect jdbc:hive2://localhost:10000 scott tiger
```

```bash
show databases;
```

```bash
create table hive_example(a string, b int) partitioned by(c int);
alter table hive_example add partition(c=1);
insert into hive_example partition(c=1) values('a', 1), ('a', 2),('b',3);
select count(distinct a) from hive_example;
select sum(b) from hive_example;
```

## ScyllaDB

### Connect to cqlsh

```bash
docker exec -it scylla-1 cqlsh
```

### Create keyspace

```cassandraql
CREATE KEYSPACE data
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};
```

### Use keyspace and create table

```cassandraql
USE data;

CREATE TABLE data.users (
    user_id uuid PRIMARY KEY,
    first_name text,
    last_name text,
    age int
);
```

### Insert data

```cassandraql
INSERT INTO data.users (user_id, first_name, last_name, age)
  VALUES (123e4567-e89b-12d3-a456-426655440000, 'Polly', 'Partition', 77);
```

## Kafka

### Create topic

```bash
docker exec -it kafka kafka-topics.sh --create --topic test --bootstrap-server 127.0.0.1:9092
```

### Kafka producer

See [kafka_producer.ipynb](notebooks/kafka_producer.ipynb)

### Kafka consumer

[kafka_consumer.ipynb](notebooks/kafka_consumer.ipynb)

## Airflow

Check out the `.env.template` file. Copy/paste airflow related variables and
update their values where necessary.

### Slack integration

You need to create a Slack app and setup `AIRFLOW_CONN_SLACK_API_DEFAULT`
env variable with Slack api key. If you don't want to use this integration,
remove the `AIRFLOW_CONN_SLACK_API_DEFAULT` variable from your `.env` file.

## Mongo
