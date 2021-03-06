# anan-repo

The project summarizes the mid term and final course assignments.
## Mid term task - batch processing:
In the mid term task we used standard batch process to retrieve twits from Tweeter via REST API. 
A Python script using the python-tweeter package enables fetching REST request for user defined cities, and term. The code lookup the city coordinate in GoogleMaps and 
generates tweet lookup filter. Based on the reply status, the scripts stores the stores the tweets in a local file and in Google bucket for further MapReduce processing.
We processed MapReduce as a service via Google bigdata service, or using local VM using Hadoop. Enabling term and stop word filtering, we updated the Hadoop WordCount.java (in-line in the code) 
At the end of the data processing we got an ordered visited words list.

Lookup cities: Colombus, Detroit, Memphis, Milwaukee, NYC.
Lookup term: "ball"

The mid term task code is listed in the src/mapreduce. The code is well explained in-line.

## Final task - stream processing:
In the final project task we were requested to use Tweeter stream API, and process the data using NoSQL server (MongoDB).
A Python script using the tweepy package enables fetching stream REST request for user defined cities, and term. The code lookup the city coordinate in GoogleMaps and 
generates tweet lookup filter. Based on the reply status, the scripts posts MongoDB update message using the following JSON message:
		{ "city": "city",       <- the user requested city 
		  "term": "term",       <- the requested term 
		  "word": "word"        <- single word listed in the tweet 
		  "date": "datetime"    <- current date and time 
		}
Enabling parallel stream processing we created docker in a local VM, and started several instances in parallel. Note that Tweeter stream API limits user to 2 streams in parallel.
Instead of using standalone MongoDB process in a VM or as a service in Google cloud, we used the free mLab service (https://mlab.com) hosted by Google. 

Lookup cities: Colombus, Detroit, Memphis, Milwaukee, NYC.
Lookup term: "ball"

The final task code is listed in the src/stream. The code is well explained in-line.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The project has three main components:
1. Hadoop word-count:
	- The project is based on sample project created by Igalia (https://github.com/dpino/Hadoop-Word-Count). 
2. Google Bigdata:
	- The bigdata requires a Google account 
3. Tweeter streams:
	- The project requires a MongoDB account in MLab (www.mlab.com) or similar MongoDB installation.
	- Use docker or install docker in your OS.

### Installing

1. Hadoop word-count:
	- Install the project and follow the instruction(https://github.com/dpino/Hadoop-Word-Count).
	- Download the project and replace the wordcount.java listed in this repository.
	- Build the Java project 
```
	./build.sh
```

## Running the project

1. Hadoop word-count:
 - Run the Python script collectTwits.py, and copy the output file to Google bucket 
```
	python collectTwits.py -l nyc -t Trump
```
 - Copy the file to the user bucket (gsutil cp [file_name] gs://my-bucke)

- Run the Java project 
```
	gsutil cp gs://my-bucke [in_file]
	./run.sh
```
   - Check the results
       For all the cities:
```
	check.sh
```
   For a single city:
```
	scheck.sh
	Sample output:
		Lookup results: nyc
		get     9
		time    6
		play    6
		&amp   6
		really  5	
			
```
2. Google Bigdata:
  - Run the Python script collectTwits.py
```
	collectTwits.py -l nyc -t Trump
```
  - Run the Bigdata instance. Set the script variables SRC_FILE="",and BUCKET_ID="" first!!!
```
	bigdata.sh
```
  - Collect and prompt the data using the Python script: count_terms.py. 
	Set the local variables bucket_id, project_id, instance_id first!!!!
```
	count_terms.py
```

3. Tweeter streams:
  - Copy the project files Dockerfile, requirements.txt, and twitStream.py to a new directory
   - Build the docker
```
	docker build -t twit .
```
   - Run the docker with two arguments: -l [location] -t [term]
```
	sudo docker run -t twit -l nyc -t Trump
```
   - Aggregate the results:
```
	python aggr.py
	
	Sample output:
		Total word count for the city:  Milwaukee
		Word: RT count: 1768
		Word: Dragon count: 547
		Word: voice count: 371
		Word: Spongebob count: 370
```


## MapReduce vs. mongo DB
Comparing MapReduce vs. MongoDB pipelining based on the knowledge we gained in this work:
1.	Evaluating the overall data collected process by both approaches, we were able to collect few tenth Twit records per city/per day using the standard Tweeter REST API and MapReduce, and up to 100 records/sec using streams.
2.	MongoDB aggregation pipeline is using indexes and internal NoSQL optimizations between the aggregation steps which are not possible with MapReduce.
3.	MongoDB aggregation is more secure when the operation is triggered by user input.
4.	MapReduce supports distributed computational framework, with a distributed file system underneath for persistence. It's often used for data processing, data science, and business intelligence problems. 
5.	MapReduce usually behaves better when it is required to work with large dataset. NoSQL servers performance are DB size dependent. 
6.	MonoDB saves user defined data structure, which enables storing additional information for statistical processing. MongoDB query language supports a wide variety of queries that are much more flexible comparing MapReduce tools, which requires Java coding for specific querying.     
7.	MongoDB map/reduce is it very easy to implement comparing to MapReduce tools that requires specific system and resource configuration.
8.  We tested the Hadoop and Google BigData MapReduce applications. Both tools were written in Java, and any update required Java programming knowledge, and a wide scope of the system. MongoDB on the other hand supports flexible REST API interfaces, and a programmer can use any available tool to perform similar tasks. Therefore MongoDB is a more robust solution
9.  MongoDB is better at handling real-time data analytics. MapReduce on the other hand, excels at batch processing and long-running ETL jobs and analysis.
10. MapReduce handles data disk failure by design, MongoDB has no internal disaster recovery mechanism.
11. MapReduce systems like Hadoop determines how best to distribute work across resources in the cluster, and how to deal with potential failures in system components should they arise. MongoDB consumes resources based on the requirements. 
12. Most visited word counts comparison
	
	|MapReduce      |MongoDB stream |
	| ------------- | ------------- |
	|Nyc                       	|
	|get       9    | RT       8922	|
	|time      6    | like     1171	|
	|play      6    | &amp     1061	|
	|&amp      6    | Dragon   1023	|
	|really    5    | way       949	|
	|milwaukee                      |
	|get       9    | RT       1768	|
	|would    10    | Dragon    547	|
	|play      6    | voice     371	|
	|run       6    | Spongebob 370	|
	|fun       4    | but       370	|
	| ------------- | ------------- |
	|Memphis                        |
	|play     19    | RT       3403	|
	|time     17    | Dragon    970	|
	|get      16    | Imagine   674	|
	|like     15    | voice     672	|
	|really   14    | overs     672	|
	| ------------- | ------------- |
	|Detroit                        |
	|get      10    | RT        496 |
	|play      8    | virenderse 80 |
	|one       8    | many       75 |
	|like      8    | ImRo45     75 |
	|Im        8    | England    73 |
	| ------------- | ------------- |
	|Colombus        		|
	|like     26    | RT        753 |
	|play     19    | like      107	|
	|team     17    | &amp       74	|
	|one      17    | black      68	|
	|Im       16    | kodak      68	|
	
	Main Findings:
	1. Only the work 'like appears in both methods.
	2. 'RT' presents at all MongoDB, and 'play' in all MapReduce. 
	3. As expected stream flow generated much more hits.
	4. In mapReduce many high hits words appears in multiple cities. I MongoDB the high hits words are unique to a city.
	
13. Statistics
	MapReduce:
	1. The average daily number of tweets filtered by city and term: 20 tweets per day.
	2. Hadoop/Cloud processing time for ~ 10000 words: 12 seconds.     

	MongoDB streaming
	1. The average number tweets per second filtered by city and term: 2 tweets per second.
	2. MongoDB processing time for ~ 100000 words: ~10 seconds.     

## Class exam

### Requirements
  1. Ignore locations
  2. New term "WorldCup"
  3. Prompt 7 words

1. MapReduce updates:
	1. Update the WordCount.java file local variable: 	
		Original: private final String SEARCH_TOKEN = "Trump" ;
		New code: private final String SEARCH_TOKEN =  "WorldCup";
		
	2. In the python file we removed the location from the filter:
		twits = api.GetSearch(lang='en', count=COUNT, until=msg_days_before) 
	3. Update the check.sh: 
		Original: /usr/local/hadoop/bin/hadoop fs -cat wordcount/output/$i/* | sort -n -k2 -r | head -n5
		New code: /usr/local/hadoop/bin/hadoop fs -cat wordcount/output/$i/* | sort -n -k2 -r | head -n7
		
	Notes: 
	1. We didn't collect the tweets again.
	2. In the exam we didn't update the bigdata code and limited it to Hadoop
 1. MongoDb stream updates: 
	1. The python stream collection file: remove the locations from the filter and run it once: 
		Original: sapi.filter(track=term, languages=["en"], )
		New code: sapi.filter(locations=[slng, slat, nlat, nlat], track=[term], languages=["en"])

	2. Update the MongoDb aggregation python file, remove the match rule:
		Original: tweets_list = twitsTable.aggregate(
        [{"$match": {"city": city}}, {"$group": {"_id": "$word", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}])
		 
		New code: tweets_list = twitsTable.aggregate(
        [{"$group": {"_id": "$word", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}])
	
The code is located in src/exam
	
 
## Versioning

Only master branch is supported. 

## Authors

* **James Richradson** - *Initial work* 

## License

This project is licensed under the License of each public module. Propriety code is licensed free.

## Acknowledgements

* Anyone whose code was used
