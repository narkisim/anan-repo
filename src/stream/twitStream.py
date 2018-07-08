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

CONSUMER_KEY = 'CONSUMER_KEY'
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'


uri = "MONGODB ADDRESS:PORT"
MONGO_TWITS_DB = 'twits'

# define the listener callback function
class StdOutListener(StreamListener):
    def __init__(self, city, term):
        self.cnt = 0
        self.window_start = round(datetime.datetime.utcnow().timestamp())
        self.window_end = round(datetime.datetime.utcnow().timestamp())
        self.stopWords = set(stopwords.words('english'))
        self.term = term
        self.city = city
        # remove Punctuation markers
        self.translator = str.maketrans('', '', string.punctuation)
        # create MongoDB client and connect the server
        self.mongo_client = pymongo.MongoClient(uri)
        self.db = self.mongo_client.mdb
        self.twitsTable =self.db.MONGO_TWITS_DB

    # define the database record structure
    def create_mongo_message(self, city, term, word):

        post_data = {
            'date': datetime.datetime.utcnow(),
            'city': city,
            'term': term,
            'word': word
        }
        return post_data

    # set the twit replies to MongoDB
    def update_mongodb(self, records_list):
        try:
            post_result = self.twitsTable.insert_many(records_list)
        except Exception as e:
            print (str(e))

    def on_data(self, data):
        try:
            # get the json twits entry
            data = json.loads(data)
            # check if the entry exists
            if data.get('text', 0):
                records_list = []
                twit_text = data.get('text')
                # tokenize the twit
                words = str(twit_text).split()

                # eliminate stop words
                for word in words:
                    # check if the twit words are valid i.e. skip the term and the host, and check for valid size 
                    if len(word) > 1 and word.lower() != self.term \
                            and word.lower() not in self.stopWords and not word.startswith('http'):
                        # add the word to the list
                        records_list.append(self.create_mongo_message(self.city, self.term, word))

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
    parser.add_argument('-l', '--locations', nargs='+', default=['nyc'], help='Locations list')
    parser.add_argument('-t', '--term', nargs='+', default=['Trump'], help='search token')
    args = parser.parse_args()

    # extract the the filter parameters i.e. the city and the term
    locations = args.locations
    # get only the first term
    location = locations[0]
    print("Requested location: {0}".format(location))
    # get only the first term
    term = str(args.term[0]).lower()
    print("Requested term: {0}".format(term))

    return location, term

# get the city coordinates from Google
def get_city_coordinates(location):
    # generate the google map requests for the given locations
    request_line = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location
    req = requests.get(request_line)
    # get the json response
    cords = req.json()
    if cords['status'] == 'OK':
        try:
            # process the responses and extract the location (assuming that the reply uses fix json format
            nlat = cords['results'][0]['geometry']['bounds']['northeast']['lat']
            nlng = cords['results'][0]['geometry']['bounds']['northeast']['lng']
            slat = cords['results'][0]['geometry']['bounds']['southwest']['lat']
            slng = cords['results'][0]['geometry']['bounds']['southwest']['lng']
            print ("Google response OK")
            return nlat, nlng, slat, slng
        except:
            # fall down and use the default location
            pass
        
    # if failed return the default location NYC
    print("Google lookup failed")
    return 40.9175771, -73.70027209999999, 40.4773991, -74.25908989999999


if __name__ == '__main__':

    # download the NLTK stop word library
    nltk.download('stopwords', quiet=True)
    stopWords = set(stopwords.words('english'))

    # get the script arguments
    location, term = get_arguments()

    # get the requested city coordinates
    nlat, nlng, slat, slng = get_city_coordinates(location)

    # create the twitter listener
    listener = StdOutListener(location, term)
    # authenticate twitter application
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # add the twitter filters
    api = tweepy.API(auth)
    sapi = tweepy.streaming.Stream(auth, listener, tweet_mode='extended')
    # set the filter by locations term and limited to English
    sapi.filter(locations=[slng, slat, nlng, nlat], track=[term], languages=["en"])
