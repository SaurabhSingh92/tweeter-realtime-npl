from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, IntegerType, StringType
import json

if __name__ == '__main__':

    spark = SparkSession.builder. \
        master('local'). \
        appName('Kafka_tweet_sentiment')\
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("Starting the read")

    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option('subscribe', 'twitter')\
        .option("startingOffsets", 'earliest')\
        .load()

    df.printSchema()

    schema = StructType().add("id", IntegerType())\
        .add("name", StringType()).add("city", StringType()).add("country", StringType())

    query = df.selectExpr("CAST(value AS STRING)")\
        .select(from_json("value", schema).alias("tweet"))\
        .select("tweet.*")\
        .writeStream\
        .format("console") \
        .outputMode("append").trigger(processingTime='5 seconds')\
        .start()

    query.awaitTermination()

    print("Stream Data Processing Application Completed.")
