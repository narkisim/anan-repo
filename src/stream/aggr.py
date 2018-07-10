from tweepy import OAuthHandler
import datetime
import pymongo
import argparse
import unicodedata
from bson.code import Code
from bson.son import SON
import pprint

# MongoDB hosting URL: https://mlab.com/home
CONSUMER_KEY = "CONSUMER_KEY"
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

uri = "mongodb://IP:PORT"
MONGO_TWITS_DB = 'twits'
DATE = datetime.datetime(2018, 7, 1, 0, 0, 0)

ONE = 1
N = 5

# connect to MongoDB
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
mongo_client = pymongo.MongoClient(uri)
db = mongo_client.mdb
twitsTable = db[MONGO_TWITS_DB]

# twitsTable.remove({"term": ["ball"]})

location_list = ['Milwaukee', 'Memphis', 'Colombus', 'Detroit', 'nyc']

#  scan all the cities and aggregate the results based on the selected word
#  scan all the cities and aggregate the results based on the selected word
for city in location_list:
    idx = 0
    print ("Total word count for the city: ", city)
    # aggregate the word and count
    tweets_list = twitsTable.aggregate(
        [{"$match": {"city": city}}, {"$group": {"_id": "$word", "total": {"$sum": 1}}},{"$sort": {"total": -1}}])
    # scan the aggregation results and print the top N (N=5)
    for tweets in tweets_list:
        tweet_text = str(unicodedata.normalize('NFKD', tweets['_id']).encode('ascii', 'ignore'))
        print ("Word: {0} count: {1}".format(tweet_text, tweets['total']))
        idx += 1
        if idx >= N:
            break
