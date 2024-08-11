from pyspark.sql import SparkSession
import pandas as pd

import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", type=str, help="Inside Airbnb data url")
    return parser.parse_args()


spark = SparkSession.builder.appName("airbnb").getOrCreate()
sc = spark.sparkContext

args = get_args()
df = spark.createDataFrame(pd.read_csv(args.url))

print(f"# of rows: {df.count()}")
df.show(20)
