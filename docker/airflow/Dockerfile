FROM apache/airflow:2.9.1-python3.12

USER root
RUN apt-get update && apt-get install -y curl wget vim

RUN wget --no-verbose -O openjdk-11.tar.gz https://builds.openlogic.com/downloadJDK/openlogic-openjdk/11.0.11%2B9/openlogic-openjdk-11.0.11%2B9-linux-x64.tar.gz
RUN tar -xzf openjdk-11.tar.gz --one-top-level=openjdk-11 --strip-components 1 -C /usr/local
ENV JAVA_HOME=/usr/local/openjdk-11
# ENV SPARK_WORKLOAD=submit

ENV SPARK_VERSION=3.5.1 \
HADOOP_VERSION=3 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

RUN mkdir ${SPARK_HOME} && chown -R "${AIRFLOW_UID}:0" "${SPARK_HOME}"

USER airflow

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p ${SPARK_HOME} \
&& tar -xf apache-spark.tgz -C ${SPARK_HOME} --strip-components=1 \
&& rm apache-spark.tgz

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV PYSPARK_PYTHON=/usr/bin/python3
