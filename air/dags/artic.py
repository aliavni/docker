import logging
from datetime import datetime

import pymongo
import requests
from airflow.decorators import dag

from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from pymongo import MongoClient, UpdateOne
from pymongo.collection import Collection
from pymongo.database import Database


@dag(
    dag_id="artic",
    schedule=None,
    start_date=datetime(2024, 6, 21),
    catchup=False,
)
def artic() -> None:
    pass


def get_art_data_and_write_to_mongo():
    endpoint = "https://api.artic.edu/api/v1/artworks?limit=100"

    hook = MongoHook(mongo_conn_id="mongo_default")
    client: MongoClient = hook.get_conn()
    db: Database = client.get_database("artic")
    collection: Collection = db.get_collection("art")

    collection.create_index([("id", pymongo.ASCENDING)], unique=True)

    page = 1
    pieces = 0
    while True:
        logging.info(f"working on page {page}")
        resp = requests.get(endpoint, timeout=60)
        resp_json = resp.json()

        data = resp_json.get("data", [])
        if len(data) == 0:
            break

        pieces += len(data)

        # Upsert to mongo
        ops = [
            UpdateOne({"id": piece["id"]}, {"$set": piece}, upsert=True)
            for piece in data
        ]
        collection.bulk_write(ops)

        pagination = resp_json.get("pagination", {})
        endpoint = pagination.get("next_url")

        if not endpoint:
            break

        page += 1

    logging.info(f"Finished. Made {page} API calls. Upserted {pieces}.")


dag = artic()

get_art_data = PythonOperator(
    task_id="get_art_data", dag=dag, python_callable=get_art_data_and_write_to_mongo
)
