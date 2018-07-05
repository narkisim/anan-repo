#!/bin/bash

# /usr/local/hadoop/bin/hadoop fs -cat ~/wordcount/output/* | grep 'with\|what'
# /usr/local/hadoop/bin/hadoop fs -cat ~/wordcount/output/* | sort -n -k2 -r | head -n5 > Top-5.txt

# declare the location array
cities=("nyc" "boston" "miami" "austin")
## now loop through the above array
for i in "${cities[@]}"
do
   echo "Lookup results: $i"
   /usr/local/hadoop/bin/hadoop fs -cat wordcount/output/$i/* | sort -n -k2 -r | head -n5
done 
