# builder step used to download and configure spark environment
FROM openjdk:11.0.11-jre-slim-buster as builder

# Add Dependencies for PySpark and Python 3.11
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates \
    build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev \
    libffi-dev libsqlite3-dev libbz2-dev rsync

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.5.1 \
HADOOP_MAJOR_VERSION=3 \
HADOOP_VERSION=3.4.0 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_MAJOR_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz

# Install Python 3.11
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.11.5/Python-3.11.5.tgz \
    && tar -xf Python-3.11.5.tgz \
    && cd Python-3.11.5 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall
RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3.11)" 1
RUN update-alternatives --install "/usr/bin/python3" "python3" "$(which python3.11)" 1

RUN rm -rf /tmp/Python-3.11.5
RUN rm /tmp/Python-3.11.5.tgz

# Hadoop
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
RUN mkdir -p /home/hadoop/
RUN groupadd hadoop
RUN useradd -d /home/hadoop -g hadoop -m hadoop --shell /bin/bash

RUN apt-get install -y pdsh openssh-client openssh-server

RUN mkdir /home/hadoop/.ssh
RUN ssh-keygen -t rsa -P '' -f /home/hadoop/.ssh/id_rsa
RUN cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys
RUN chmod 0600 /home/hadoop/.ssh/authorized_keys

COPY ssh/config /home/hadoop/.ssh/config
RUN service ssh start

RUN chown -R hadoop:hadoop $HADOOP_HOME
RUN chown -R hadoop:hadoop /home/hadoop

USER hadoop
ENV JAVA_HOME=/usr/local/openjdk-11
USER root
COPY requirements.txt /tmp/requirements.txt

ENV PATH=/opt/spark/bin:$PATH

RUN chown -R hadoop:hadoop /opt/spark
RUN ln -sf /bin/bash /bin/sh

# Venv
RUN cd /usr/local \
    && python -m venv pyspark_venv \
    && . pyspark_venv/bin/activate \
    && pip install -r /tmp/requirements.txt

WORKDIR /opt/spark

USER hadoop

# Apache spark environment
FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 6066 10000

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

COPY start-spark.sh /
RUN wget -P /opt/spark/jars https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

RUN echo "alias ls='ls --color=auto'" >> /home/hadoop/.bashrc
RUN echo "alias l='ls -lah'" >> /home/hadoop/.bashrc
RUN echo "alias ll='ls -lh'" >> /home/hadoop/.bashrc
RUN echo "alias la='ls -lAh'" >> /home/hadoop/.bashrc

CMD ["/bin/bash", "/start-spark.sh"]
