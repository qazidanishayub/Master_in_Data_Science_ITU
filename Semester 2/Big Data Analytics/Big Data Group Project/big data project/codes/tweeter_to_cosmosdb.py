#pip install azure-cosmos
import json
import tweepy
from datetime import datetime
from dateutil import parser
import json
import re
import time

from azure.cosmos import CosmosClient, exceptions
import os

url = "https://bd-tweets-trends.documents.azure.com:443/"
key = "06k6c3UAFb10Fpdd0BlXBPm31pw3mYLvTCez0dFSuyNlFBynRi0140L0gDkURoaSq8x1yaOdh1IGfddImEp1Qg=="
client = CosmosClient(url, credential=key)

database_name = 'tweets'
database = client.get_database_client(database_name)
container_name = 'general'
container = database.get_container_client(container_name)




def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api,time_limit):
        self.api = api
        self.me = api.me()
        self.start_time = time.time()
        self.limit = time_limit
        #self.saveFile = open('last.json', 'a')

    def on_status(self, tweet):
  
        strt=tweet.text
        if(len(str(strt))>120 and ('#' in str(strt))):
            
            print("------------------"+str(len(strt))+"---------------------------")
            tweet_text=strt
            if strt.find(":") != -1:
                str2=strt.split(':')
                tweet_text=str2[1]
                print(tweet.created_at)
                #new_datetime = datetime.strptime(str(tweet.created_at),'%a %b %d %H:%M:%S')

            data={'user':tweet.user.name,
                  'created_at':str(tweet.created_at),
                  'location':tweet.user.location,
                  'friends_count':tweet.user.friends_count,
                  'followers_count':tweet.user.followers_count,
                  'tweet':tweet_text}
            print(data)
            if (time.time() - self.start_time) < self.limit:
                #self.saveFile.write(json.dumps(data))
                #self.saveFile.write('\n')
                #client.send_batch(event_data_batch)
                container.upsert_item(data)
                return True
            else:
                #self.saveFile.close()
                return False      

    def on_error(self, status):
        print("Error detected")

# Authenticate to Twitter
consumer_key = "Ov4U9iugguLjBFRZi65e5RtKc"
consumer_secret = "mLEGsS8WN2pPAAHbj8xEMrSV52FrDxjAsrNmECx8uzXyitVNe6"
access_token = "2647039968-ErCWB3aJkORwrEbz7GoKcqlnrbP3Lrc5aIJ8TVN"
access_token_secret = "kIvX5eDRl0gBARZtdzKYFbYFuUqJ3UV5H5YEruk9GmhBa"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api,10)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["TikTok",
"BreakingNews",
"Israel",
"Ronaldo",
"Michael Holding",
"Pfizer",
"AstraZeneca",
"johar town",
"Sinopharm",
"Delta",
"Kazuya"
"Wimbledon", 
"Djokovic",
"Court",
'VenmoMe',
'Tekken',
'Master Chief',
'Mii Fighter',
'Atticus Ross',
'SPACE BOOTZ',
'Big Foe',
'SPACE',
'Big Bang Theory',
'Mimobiles',
'Window 11',
'Ivanka Trump',
'Sajid Javid',
'ToryCorruptCabal',
'Giggs'
'Serco'
], languages=["en"])