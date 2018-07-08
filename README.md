# anan-repo

The project summarizes the mid term and final course assignments 

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
	mvn clean install
```

## Running the project

1. Hadoop word-count:
	- Run the Python script collectTwits.py, and copy the output file to Google bucket 
```
	collectTwits.py -l nyc -t Trump
	gsutil cp [file_name] gs://my-bucke
```
	- Run the Java project 
```
	gsutil cp gs://my-bucke [in_file]
	mvn exec:java -Dexec.mainClass=com.igalia.wordcount.App [in_file] [out_file] [term]
```
	- Check the results
```
	check.sh
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
	- Collect and prompt the data using the Python script: count_terms.py. Set the local variables bucket_id, project_id, instance_id fisrt!!!!
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

## MapReduce vs. mongo DB
Comparing MapReduce vs. MongoDB pipelining based on the knowledge we gained in this work:
1.	Evaluating the overall data collected process by both approaches, we were able to collect few tenth Twit records per city/per day using the standard Tweeter REST API and MapReduce, and up to 100 records/sec using streams.
2.	MongoDB aggregation pipeline is using indexes and internal NoSQL optimizations between the aggregation steps which are not possible with MapReduce.
3.	MongoDB aggregation is more secure when the operation is triggered by user input.
4.	MapReduce supports distributed computational framework, with a distributed file system (HDFS) underneath for persistence.  It's often used for data processing, ETL, data science, and business intelligence problems. 
5.	MapReduce usually behaves better when it is required to work with large dataset. 
6.	MonoDB saves user defined data structure, which enables storing additional information for statistical processing. MongoDB query language supports a wide variety of queries that are much more flexible comparing MapReduce tools, which requires Java coding for specific querying.     
7.	MongoDB map/reduce is it is very easy to implement comparing to MapReduce tools that requires specific system and resource configuration.


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **James Richradson** - *Initial work* 

## License

This project is licensed under the License of each public module. Propriety code is licensed free.

## Acknowledgments

* Anyone whose code was used
