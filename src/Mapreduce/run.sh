#!/bin/bash

rm -rf $(pwd)/wordcount/output
# copy files from bucket
gsutil cp gs://MY_BUCKET/*.txt ~/wordcount/input
# declare the location array
cities=("nyc" "boston" "miami" "austin")

## now loop through the above array
for i in "${cities[@]}"
do
   echo "Lookup: $i"
   # execute the python script
   # python ~/cloud/python/twits.py -l $i
   python python/twits.py -l $i
   # do the map-reduce
   mvn exec:java -Dexec.mainClass=com.igalia.wordcount.App -Dexec.args="wordcount/input/$i/ wordcount/output/$i/"
   # /usr/local/hadoop/bin/hadoop jar target/wordcount-0.0.1-SNAPSHOT.jar ~/wordcount/input/$i/ ~/wordcount/output/$i/
done 
