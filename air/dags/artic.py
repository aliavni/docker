"""This script defines an Apache Airflow DAG for fetching artwork data from the
Art Institute of Chicago API and storing it in a MongoDB collection. The DAG is
named "artic" and does not have a predefined schedule.

Functions:
----------
- artic: Defines the Airflow DAG structure.
- get_art_data_and_write_to_mongo: Fetches artwork data from the Art Institute of Chicago API,
    processes it, and upserts it into a MongoDB collection.

Key Components:
---------------
- MongoHook: Used to establish a connection to the MongoDB instance.
- pymongo: Provides MongoDB operations such as creating indexes and performing bulk writes.
- requests: Used to make HTTP GET requests to the Art Institute of Chicago API.
- PythonOperator: Executes the `get_art_data_and_write_to_mongo` function as part of the DAG.

Workflow:
---------
1. The DAG starts execution from the defined `start_date` and does not catch up on missed runs.
2. The `get_art_data_and_write_to_mongo` function fetches artwork data in paginated form from the API.
3. Each piece of artwork data is upserted into the MongoDB collection with a unique index on the "id" field.
4. The process continues until all pages of data are fetched and stored.

Logging:
--------
- Logs the current page being processed.
- Logs the total number of API calls made and the number of pieces of artwork upserted.

MongoDB Collection:
-------------------
- Database: `artic`
- Collection: `art`
- Index: Unique index on the "id" field.

Airflow DAG:
------------
- DAG ID: "artic"
- Task: "get_art_data" (Executes the `get_art_data_and_write_to_mongo` function)
"""

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
    """Fetch artwork data from the Art Institute of Chicago API, process it,
    and upsert it into a MongoDB collection."""
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
