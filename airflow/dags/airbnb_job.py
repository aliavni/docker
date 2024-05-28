from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder.appName("airbnb").getOrCreate()
sc = spark.sparkContext

url = "https://data.insideairbnb.com/united-states/ma/boston/2024-03-24/data/listings.csv.gz"

df = spark.createDataFrame(pd.read_csv(url))

print(f"# of rows: {df.count()}")

df.show(20)
