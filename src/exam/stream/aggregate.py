from tweepy import OAuthHandler
import pymongo
import unicodedata

# MongoDB hosting URL: https://mlab.com/home
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

uri = "mongodb://IP:PORT"
MONGO_TWITS_DB = 'twitsNc'

N = 7

# connect to MongoDB
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
mongo_client = pymongo.MongoClient(uri)
db = mongo_client.mdb
twitsTable = db[MONGO_TWITS_DB]


#  scan all the cities and aggregate the results based on the selected word
idx = 0
tweets_list = twitsTable.aggregate(
        [{"$group": {"_id": "$word", "total": {"$sum": 1}}},
         {"$sort": {"total": -1}}])
# scan the aggregation results and print the top N (N=5)
for tweets in tweets_list:
     tweet_text = str(unicodedata.normalize('NFKD', tweets['_id']).encode('ascii', 'ignore'))
     print ("Word: {0} count: {1}".format(tweet_text, tweets['total']))
     idx += 1
     if idx > N:
         break
