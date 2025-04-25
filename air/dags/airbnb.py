"""Airflow DAG to fetch and process Airbnb data from a given URL."""

from datetime import datetime

import pandas as pd
import pymongo
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.sdk import DAG, task

# from airflow.providers.slack.notifications.slack import send_slack_notification

BASE_URL = "https://data.insideairbnb.com/"


with DAG(
    dag_id="airbnb",
    params={
        "url": BASE_URL + "united-states/ma/boston/2025-03-15/data/listings.csv.gz"
    },
    schedule=None,
    start_date=datetime(2024, 5, 20),
    catchup=False,
    # on_success_callback=[
    #     send_slack_notification(
    #         text=""":large_green_circle: `{{ dag.dag_id }}` dag succeeded at `{{ macros.datetime.utcnow() }}`
    #         *processed:* {{ params.url }}
    #         """,
    #         channel="#airflow-alerts",
    #         username="Airflow",
    #     )
    # ],
) as dag:

    @task.python
    def get_and_process_data() -> None:
        """Fetch and process data from the given URL."""
        df = pd.read_csv(dag.params["url"])

        hook = MongoHook(mongo_conn_id="mongo_default")
        client: pymongo.MongoClient = hook.get_conn()
        db: pymongo.database.Database = client.get_database("airbnb")
        collection: pymongo.collection.Collection = db.get_collection("listings")

        collection.create_index([("id", pymongo.ASCENDING)], unique=True)

        listings = df.to_dict(orient="records")

        ops = [
            pymongo.UpdateOne({"id": listing["id"]}, {"$set": listing}, upsert=True)
            for listing in listings
        ]
        collection.bulk_write(ops)

    get_and_process_data()
