import os
import twitter
import requests
import argparse
import unicodedata
from datetime import datetime, timedelta
from os.path import expanduser

home = expanduser("~")

N_DAYS = 6
COUNT = 10000
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


# set the default locations list
default_location_list = ['nyc', 'washington', 'austin', 'miami']

# the command arguments are: -l "amsterdam", "london", "paris"
parser = argparse.ArgumentParser(description='Twitter application sample interface')
parser.add_argument('-l', '--locations', nargs='+', default=default_location_list, help='Locations list')
args = parser.parse_args()

location_list = []
for index, loc in enumerate(args.locations):
    print ("loc = ", loc)
    location_list.append(loc)

# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

# scan all locations and retrieve data
for location in location_list:
    # generate the google map requests for the given locations
    request_line = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location
    req = requests.get(request_line)
    # set the date (up to 7 days is a Twitter limitation)
    days_before = datetime.now() - timedelta(days=N_DAYS)  # YYYY-MM-DD.
    msg_days_before = days_before.strftime('%Y-%m-%d')

    # get the json response
    cords = req.json()
    if cords['status'] == 'OK':
	print ("Google response OK")
        # process the responses and extract the location
        lat = cords['results'][0]['geometry']['bounds']['northeast']['lat']
        lng = cords['results'][0]['geometry']['bounds']['northeast']['lng']
        # fetch the twitter search
        twits = api.GetSearch(geocode=[lat, lng, '10km'],lang='en', count=COUNT, until=msg_days_before)
    else:
        print ("Twitter direct response OK")
        twits = api.GetSearch(location, lang='en', count=COUNT, until=msg_days_before)
    # set the output filename
    # folder_name = home +'/cloud/Hadoop-Word-Count-master/wordcount/input/' + location
    folder_name = 'wordcount/input/' + location
    try:
        # check if the folder exists
        os.stat(folder_name)
    except:
        # the folder is missing, create one
        os.mkdir(folder_name)
    # define the filename
    file_name = folder_name + '/twit.txt'
    out_file = open(file_name, 'w')


    for twit in twits:
        # convert from unicode to UTF8. It is required by the map-reduce
        utf_text = unicodedata.normalize('NFKD', twit.text).encode('ascii', 'ignore')
        # write the data to file
        out_file.write(utf_text)
    out_file.close()
 
