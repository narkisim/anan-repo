from tweepy import OAuthHandler
import datetime
import pymongo
import argparse

# MongoDB hosting URL: https://mlab.com/home
CONSUMER_KEY = "CONSUMER_KEY"
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_TOKEN = 'ACCESS_TOKEN-2Lnmq98pYyOdRwmCPE6XqRniKXLV7DC'
ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

uri = "mongodb://IP:PORT"
MONGO_TWITS_DB = 'twits'
DATE = datetime.datetime(2018, 7, 1, 0, 0, 0)

# connect to MongoDB
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
mongo_client = pymongo.MongoClient(uri)
db = mongo_client.mdb
twitsTable = db[MONGO_TWITS_DB]

parser = argparse.ArgumentParser(description='MongoDB sample interface')
parser.add_argument('-t', '--word', nargs='+', default=['guess'], help='search word')
args = parser.parse_args()
word = str(args.term[0]).lower()
print("Requested term = ", word)

# sample update code
# query = {'city': 'nyc'}
# twitsTable.update(query, {'$set': {'city': 'New York'}})


# query and count example
# count by city
nyc_count = twitsTable.find({'city': 'nyc'}).count()
print("Total count for : {0} is {1}".format('Nyc', nyc_count))
# count by city and word search
nyc_count = twitsTable.find({'city': 'nyc', 'word' : word}).count()
print("Total for city: {0}, and word: {1} is {2}".format('Nyc', word, nyc_count))
# count by date bigger
day_count = db.collection.find({'city': 'nyc', 'date': {'$gte': DATE}}).count()
print("Total count for : {0} from date: {1} is {2}".format('Nyc', DATE.strftime("%Y-%m-%d %H:%M"),nyc_count))

# run a query which returns all the hits for a specific city
# .sort([("field1", pymongo.ASCENDING), ("field2", pymongo.DESCENDING)])
returned_list = twitsTable.find({'city': 'nyc','date': {'$gte': DATE}}).sort([("date", pymongo.ASCENDING)])
for doc in returned_list:
print('Nyc dated {0} the word {1} and the trem {2} .'.format(doc['date'], doc['word'], doc['term']))
