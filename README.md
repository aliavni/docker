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
