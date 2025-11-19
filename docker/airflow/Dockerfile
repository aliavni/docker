FROM apache/airflow:3.1.3-python3.10
# FROM --platform=linux/amd64 apache/airflow:3.0.0-python3.9

USER root
RUN apt-get update && apt-get install -y curl wget vim procps less

# TODO: Try using https://download.java.net/java/GA/jdk24.0.1/24a58e0e276943138bf3e963e6291ac2/9/GPL/openjdk-24.0.1_linux-x64_bin.tar.gz
RUN wget --no-verbose -O openjdk-11.tar.gz https://builds.openlogic.com/downloadJDK/openlogic-openjdk/11.0.11%2B9/openlogic-openjdk-11.0.11%2B9-linux-x64.tar.gz
RUN tar -xzf openjdk-11.tar.gz --one-top-level=openjdk-11 --strip-components 1 -C /usr/local
ENV JAVA_HOME=/usr/local/openjdk-11
# ENV SPARK_WORKLOAD=submit

ENV SPARK_VERSION=3.5.7 \
    HADOOP_VERSION=3 \
    SPARK_HOME=/opt/spark \
    PYTHONHASHSEED=1

RUN mkdir ${SPARK_HOME} && chown -R "${AIRFLOW_UID}:0" "${SPARK_HOME}"

USER airflow

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    && mkdir -p ${SPARK_HOME} \
    && tar -xf apache-spark.tgz -C ${SPARK_HOME} --strip-components=1 \
    && rm apache-spark.tgz

COPY requirements.txt /tmp/requirements.txt
RUN uv pip install -r /tmp/requirements.txt

USER root

COPY requirements_spark.txt /tmp/requirements_spark.txt
RUN cd /usr/local \
    && python -m venv pyspark_venv \
    && . pyspark_venv/bin/activate \
    && uv pip install -r /tmp/requirements_spark.txt

USER airflow

ENV PYSPARK_PYTHON=/usr/local/pyspark_venv/bin/python
