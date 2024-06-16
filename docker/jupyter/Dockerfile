FROM jupyter/base-notebook:python-3.11.5

USER root
RUN apt-get update && apt-get install -y openjdk-8-jdk-headless wget

RUN mkdir -p /opt/spark/jars
RUN wget -P /opt/spark/jars https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
RUN chown jovyan /opt/spark/jars/postgresql-42.7.3.jar

USER jovyan

WORKDIR /home/jovyan

COPY ./requirements.txt /tmp/requirements.txt

RUN export DOCKER_BUILDKIT=1

RUN conda install -y -c conda-forge mamba
RUN mamba install -y --file /tmp/requirements.txt
