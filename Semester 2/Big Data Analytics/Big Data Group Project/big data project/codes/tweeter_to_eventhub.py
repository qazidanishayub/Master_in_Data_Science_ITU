import json
import tweepy
from datetime import datetime
from dateutil import parser
import json
import re
import time
from azure.eventhub import EventHubProducerClient, EventData

connection_str = 'Endpoint=sb://bd-project.servicebus.windows.net/;SharedAccessKeyName=bd;SharedAccessKey=8O9dtqUrGfm7/Eig9nvmsKDVuHw0DJUyaCs0bOVvz54=;EntityPath=tweets'
eventhub_name = 'tweets'
client = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

event_data_batch = client.create_batch()
#can_add = True
#count=0
#while can_add:
#    try:
#        count=count+1
#        event_data_batch.add(EventData('Message inside EventBatchData'+str(count)))
#    except ValueError:
#        can_add = False  # EventDataBatch object reaches max_size.

#with client:
#    client.send_batch(event_data_batch)


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
                event_data_batch.add(EventData(json.dumps(data)))
                #client.send_batch(event_data_batch)
                return True
            else:
                #self.saveFile.close()
                client.send_batch(event_data_batch)
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
stream.filter(track=["Bitcoin",
"Elon Musk",
"Bigdata",
"Spark",
"Hadoop",
"Python",
"PHP",
"Azure",
"AWS",
"ICC",
"Windows"
"Search engine", 
"Security"
"WordPress"
], languages=["en"])