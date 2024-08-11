import os
from datetime import datetime

from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.decorators import dag


@dag(
    dag_id="anatomy",
    schedule=None,
    start_date=datetime(2024, 5, 30),
    catchup=False,
)
def anatomy() -> None:
    """
    # Anatomy of a DAG
    """
    pass


dag = anatomy()


def pull_data_callable():
    return [{"id": 1}, {"id": 2}]


pull_data = PythonOperator(
    task_id="pull_data", python_callable=pull_data_callable, dag=dag
)

process_data = SparkSubmitOperator(
    conn_id="spark_master",
    application=os.path.abspath("dags/process_data.py"),
    task_id="process_data",
    dag=dag,
)

process_data.ui_color = "white"
pull_data.ui_color = "white"

write_to_s3 = S3CreateObjectOperator(
    task_id="write_to_s3", s3_key="my_file", data=process_data.output
)

pull_data >> process_data >> write_to_s3

# dag.get_task("process_data") >> process_data
