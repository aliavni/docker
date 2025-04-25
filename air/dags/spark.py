"""Example Spark DAG."""

import os
from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

dag = DAG("spark_job_example", start_date=datetime(2024, 5, 20), schedule="@once")

spark_task = SparkSubmitOperator(
    conn_id="spark_master",
    application=os.path.abspath("dags/spark_job.py"),
    task_id="run_spark_job",
    dag=dag,
)
