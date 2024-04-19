## trino

```
docker exec -it trino trino
```

```
SHOW SCHEMAS FROM db;
```

```
USE db.public;
```

```
SHOW TABLES FROM public;
```

## spark

```
docker exec -it spark-master /bin/bash
```

```
cd /opt/spark/bin
./spark-submit --master spark://0.0.0.0:7077 --name spark-pi --class org.apache.spark.examples.SparkPi  local:///opt/spark/examples/jars/spark-examples_2.12-3.5.1.jar 100
```

## thrift

In spark-master:

```
./bin/beeline
```

```
!connect jdbc:hive2://localhost:10000 scott tiger
```

```
show databases;
```

```
create table hive_example(a string, b int) partitioned by(c int);
alter table hive_example add partition(c=1);
insert into hive_example partition(c=1) values('a', 1), ('a', 2),('b',3);
select count(distinct a) from hive_example;
select sum(b) from hive_example;
```
