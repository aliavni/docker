# Docker data stack

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Run](#run)
- [Jupyter](#jupyter)
- [Trino](#trino)
- [Spark](#spark)
- [Thrift](#thrift)

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
