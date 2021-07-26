from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, udf
from pyspark.sql.types import StructType, StringType
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def sentance_analyze(sent):
    score = SentimentIntensityAnalyzer()
    points = score.polarity_scores(f"{sent}")
    if points['compound'] > 0:
        res = 'Positive'
    elif points['compound'] < 0:
        res = 'Negative'
    else:
        res = 'Neutral'
    return res


if __name__ == '__main__':
    spark = SparkSession.builder \
        .master('local') \
        .appName('Kafka_tweet_sentiment') \
        .getOrCreate()


    spark.sparkContext.setLogLevel("ERROR")

    print("Starting the read")

    df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option('subscribe', 'twitter') \
        .option("startingOffsets", 'latest') \
        .load()

    df.printSchema()

    # fake_schema = StructType().add("id", IntegerType())\
    #     .add("name", StringType()).add("city", StringType()).add("country", StringType())

    tweet_schema = StructType().add("id", StringType()).add("tweet", StringType()) \
        .add("Creation_date", StringType()).add("UserName", StringType())

    score_cal = udf(lambda v: sentance_analyze(v), StringType())
    cov_date = udf(lambda v: datetime.strftime(datetime.strptime(v, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S'))
    df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", tweet_schema).alias("tweet")) \
        .select("tweet.*") \
        .withColumn("Score", score_cal('tweet')) \
        .withColumn("Creation_date", cov_date('Creation_date'))\
        .groupBy("Score").count()

    stream = df.writeStream \
        .format("memory") \
        .outputMode("update") \
        .queryName("sentiment") \
        .trigger(processingTime="5 Seconds").start()

    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    plt.style.use("seaborn")


    def animate(i):
        x = df.toPandas()['Score'].values.tolist()
        y = df.toPandas()['count'].values.tolist()
        ax1.bar(x, y)

    ani = FuncAnimation(fig, animate, interval=100000)
    plt.show()

    stream.awaitTermination()

    print("Stream Data Processing Application Completed.")
