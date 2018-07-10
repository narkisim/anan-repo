import os
import twitter
import requests
import argparse
import unicodedata
from datetime import datetime, timedelta
from os.path import expanduser

home = expanduser("~")

N_DAYS = 1
COUNT = 10000
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# the command arguments are: -l "amsterdam", "london", "paris"
parser = argparse.ArgumentParser(description='Twitter application sample interface')
args = parser.parse_args()
parser.add_argument('-t', '--term', nargs='+', default=['Trump'], help='search token')
args = parser.parse_args()
# get only the first term
term = str(args.term[0]).lower()
print("Requested term = ", term)


# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

# set the date (up to 7 days is a Twitter limitation)
days_before = datetime.now() - timedelta(days=N_DAYS)  # YYYY-MM-DD.
msg_days_before = days_before.strftime('%Y-%m-%d')

twits = api.GetSearch(term=term, lang='en', count=COUNT, until=msg_days_before)

file_name = 'wordcount/input/twit.txt'
out_file = open(file_name, 'a')

for twit in twits:
    if twit.text is not None:
        # convert from unicode to UTF8. It is required by the map-reduce
        utf_text = str(unicodedata.normalize('NFKD', twit.text).encode('ascii', 'ignore'))
    else:
        utf_text = str(unicodedata.normalize('NFKD', twit.full_text).encode('ascii', 'ignore'))
    # write the data to file
    record = datetime.now().strftime("%d/%m/%Y") + " " + str(utf_text)
    out_file.write(record)
out_file.close()
