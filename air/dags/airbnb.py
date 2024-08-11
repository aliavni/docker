import os
from datetime import datetime
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.slack.notifications.slack import send_slack_notification
from airflow.decorators import dag


@dag(
    dag_id="airbnb",
    params={
        "url": "https://data.insideairbnb.com/united-states/ma/boston/2024-03-24/data/listings.csv.gz"
    },
    schedule=None,
    start_date=datetime(2024, 5, 20),
    catchup=False,
    on_success_callback=[
        send_slack_notification(
            text=""":large_green_circle: `{{ dag.dag_id }}` dag succeeded at `{{ macros.datetime.utcnow() }}`
            *processed:* {{ params.url }}
            """,
            channel="#airflow-alerts",
            username="Airflow",
        )
    ],
)
def airbnb() -> None:
    """
    # Airbnb

    This dag demonstrates how to use `SparkSubmitOperator`
    """


airbnb_dag = airbnb()

spark_task = SparkSubmitOperator(
    conn_id="spark_master",
    application=os.path.abspath("dags/airbnb_job.py"),
    task_id="spark_submit",
    dag=airbnb_dag,
    application_args=["--url", "{{ params.url }}"],
)
