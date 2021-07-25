import time
import json
import kafka


if __name__ == '__main__':
    while True:
        consumer = kafka.KafkaConsumer('twitter',
                                       bootstrap_servers=['localhost:9092'],
                                       auto_offset_reset='earliest',
                                       group_id='twitter_nlp')
        print("New messages:\n\n")
        for msg in consumer:
            print(f"{msg.value}")

        time.sleep(10)
