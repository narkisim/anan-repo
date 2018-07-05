import argparse
from google.cloud import bigtable
from google.cloud import happybase
from nltk.corpus import stopwords

# get the stopwords list from NTLK library
stop_words = set(stopwords.words('english'))

bucket_id = ['MY_BUCKET']
project_id = 'PROJECT_ID'
instance_id = 'INSTANCE_ID'
N = 10

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--table', nargs='+', default = bucket_id)
args = parser.parse_args()
table_arg = args.table[0]

# set the connection parameters
client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
connection = happybase.Connection(instance=instance)

# create the instance
connection.tables()
# connect the big table
table = connection.table(table_arg[0])
table.families()

# create the words list
words = []
for key, value in table.scan():
    value = ord(value['cf:count'][2])*256 + ord(value['cf:count'][3])
    # add the term to the words lisr
    words.append((key, value))

# remove the stop words from the list
resFilter = [x for x in words if x[0].lower() not in stop_words]
# sort the list by the words count
resSort = sorted(resFilter, key=lambda x: x[1], reverse=True)
# print the N topmost entries
print(resSort[:N])

