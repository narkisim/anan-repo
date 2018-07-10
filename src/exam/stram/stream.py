import string
import argparse
import tweepy
import requests
from tweepy import OAuthHandler
import nltk
from nltk.corpus import stopwords
import datetime
from tweepy.streaming import StreamListener, json
import pymongo

# MongoDB hosting URL: https://mlab.com/home

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


uri = "mongodb://IP:PORT"
MONGO_TWITS_DB = 'twitsnc'

class StdOutListener(StreamListener):
    def __init__(self, term):
        self.cnt = 0
        self.window_start = round(datetime.datetime.utcnow().timestamp())
        self.window_end = round(datetime.datetime.utcnow().timestamp())
        self.stopWords = set(stopwords.words('english'))
        self.term = term
        # remove Punctuation markers
        self.translator = str.maketrans('', '', string.punctuation)
        # create MongoDB client and connect the server
        self.mongo_client = pymongo.MongoClient(uri)
        self.db = self.mongo_client.mdb
        self.twitsTable =self.db[MONGO_TWITS_DB]


    def create_mongo_message(self, term, word):

        post_data = {
            'date': datetime.datetime.utcnow(),
            'term': term,
            'word': word
        }
        return post_data

    def update_mongodb(self, records_list):
        # result = self.db.posts.insert_one(post_data)
        try:
            post_result = self.twitsTable.insert_many(records_list)
        except Exception as e:
            print (str(e))

    def on_data(self, data):
        try:
            self.cnt += 1
            data = json.loads(data)
            if data.get('text'):
                records_list = []
                twit_text = data.get('text')
                # tokenize the twit
                words = str(twit_text).split()
                # words = word_tokenize(data.get('text'))

                # eliminate stop words
                for word in words:
                    if word.find('…') != -1:
                        continue

                    if len(word) > 1 and word.lower() != self.term \
                            and word.lower() not in self.stopWords and not word.startswith('http'):
                        # add the word to the list
                        print(word.translate(self.translator))
                        records_list.append(self.create_mongo_message(self.term, word))

                # add records to the MongoDB
                self.update_mongodb(records_list)

        except Exception as e:
            print(e)
            return False
        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

# parse the command arguments
def get_arguments():
    # the command arguments are: -l "amsterdam", "london", "paris"
    parser = argparse.ArgumentParser(description='Twitter application sample interface')
    parser.add_argument('-t', '--term', nargs='+', default=['WorldCup'], help='search token')
    args = parser.parse_args()

    # get only the first term
    term = str(args.term[0]).lower()
    print("Requested term = ", term)

    return term

if __name__ == '__main__':

    nltk.download('stopwords', quiet=True)
    stopWords = set(stopwords.words('english'))

    # get the script arguments
    term = get_arguments()

    # create the twitter listener
    listener = StdOutListener(term)
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # add the twitter filters
    api = tweepy.API(auth)
    sapi = tweepy.streaming.Stream(auth, listener, tweet_mode='extended')
    # set the filter by locations term and limited to English
    sapi.filter(track=term, languages=["en"])
