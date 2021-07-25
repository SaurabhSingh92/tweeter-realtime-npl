import random
import time
from faker import Faker
import tweepy
from kafka import KafkaProducer
from json import dumps
import config as conf
from datetime import datetime

auth = tweepy.OAuthHandler(conf.api_key, conf.api_secret)
auth.set_access_token(conf.access_token, conf.access_token_secret)
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8')
                         )
api = tweepy.API(auth)


def search_tweet():
    search_result = api.search(q='Olympic', lang='en', rpp=1)

    for tweet in search_result:
        data = tweet._json
        tw = {
            'id': data['id'],
            'tweet': data['text'],
            'Creation_date': data['created_at'],
            'UserName': data['user']['name']
        }
        print(tw)
        producer.send('twitter', tw)
    producer.flush()


def fake_date():
    fake = Faker()
    data = {}
    for i in range(0, 5):
        data[i] = {}
        data[i]['id'] = random.randint(0, 5)
        data[i]['name'] = fake.name()
        data[i]['city'] = fake.city()
        data[i]['country'] = fake.country()
        producer.send('sample', data[i])
    print(data)
    producer.flush()


if __name__ == '__main__':
    while True:
        print("Publish new tweets: ")
        search_tweet()
        # fake_date()
        time.sleep(30)
