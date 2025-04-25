"""This script connects to a PostgreSQL database list all tables."""

import datetime
import os

import psycopg2


def fun():
    """This function prints the current date and time."""
    now = datetime.datetime.now()
    print(now)


if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=os.environ["POSTGRES_PASSWORD"],
        port=5432,
        host="docker-postgres",
    )
    conn.autocommit = True
    cursor = conn.cursor()

    sql = """
    select * from information_schema.tables
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)

    counter = 0
    while counter < 10:
        fun()
        counter += 1
