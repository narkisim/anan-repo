/*
 * Copyright (C) 2012 Igalia, S.L.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package com.igalia.wordcount;

import java.io.IOException;
import java.util.StringTokenizer;
import java.util.*;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;

/**
 * 
 * @author Diego Pino García <dpino@igalia.com>
 * 
 * Canonical implementation at http://wiki.apache.org/hadoop/WordCount
 *
 */
public class WordCount extends Configured implements Tool {

	// private final String SEARCH_TOKEN =  "love";
	// the private hash table
	private static Hashtable<String, Integer> stopWordsHash = new Hashtable<String, Integer>();

	public static class MapClass extends
			Mapper<Object, Text, Text, IntWritable> {

		private static final IntWritable ONE = new IntWritable(1);
		private Text word = new Text();

		@Override
		protected void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {

			int tokenIndex = 0;
			int searchTokenIndex = 0;
			int distanceFromToken = 0;
			String DistanceToken;
			final String SEARCH_TOKEN = args[2];

			// look for the big data token, if exists process
			if (value.toString().toLowerCase().indexOf(SEARCH_TOKEN) != -1){
				searchTokenIndex  = getWordIndex(value.toString(), SEARCH_TOKEN);
				StringTokenizer tokenizer = new StringTokenizer(value.toString());
				while (tokenizer.hasMoreTokens()) {
					String token = tokenizer.nextToken();
					// skip stop words and the searched token
					if ((isStopWordOrMark(token.toLowerCase()) == -1) && (token.toLowerCase().indexOf(SEARCH_TOKEN.toLowerCase()) == -1)){
						word.set(token);
						context.write(word, ONE);
					}
				}
			}
		}
	}
		
	public static class Reduce extends
			Reducer<Text, IntWritable, Text, IntWritable> {

		private IntWritable count = new IntWritable();

		@Override
		protected void reduce(Text key, Iterable<IntWritable> values,
				Context context) throws IOException, InterruptedException {

			int sum = 0;
			for (IntWritable value : values) {
				sum += value.get();
			}
			count.set(sum);
			context.write(key, count);
		}
	}

	public int run(String[] args) throws Exception {
		fillHashTable();
	        Job job = new Job(getConf());
		job.setJarByClass(WordCount.class);
		job.setJobName("wordcount");
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		
        	job.setMapperClass(MapClass.class);
	        job.setReducerClass(Reduce.class);

		Path filePath = new Path(args[0]);
		FileInputFormat.setInputPaths(job, filePath);
		Path outputPath = new Path(args[1]);
		FileOutputFormat.setOutputPath(job, outputPath);

		boolean success = job.waitForCompletion(true);
		return success ? 0 : 1; 
	}

	// new exercise code
	private void fillHashTable(){
			final String stopWords = "i\ta\tme\tmy\tmyself\twe\tour\tours\tourselves\tyou\tyour\tyours\tyourself" +
			"\tyourselves\the\thim\this\thimself\tshe\ther\thers\therself\tit\tits\titself\tthey\tthem\ttheir" +
			"\ttheirs\tthemselves\twhat\twhich\twho\twhom\tthis\tthat\tthese\tthose\tam\tis\tare\twas\twere\tbe" +
			"\tbeen\tbeing\thave\thas\thad\thaving\tdo\tdoes\tdid\tdoing\ta\tan\tthe\tand\tbut\tif\tor\tbecause\tas" +
			"\tuntil\twhile\tof\tat\tby\tfor\twith\tabout\tagainst\tbetween\tinto\tthrough\tduring\tbefore\tafter" +
			"\tabove\tbelow\tto\tfrom\tup\tdown\tin\tout\ton\toff\tover\tunder\tagain\tfurther\tthen\tonce\there" +
			"\tthere\twhen\twhere\twhy\thow\tall\tany\tboth\teach\tfew\tmore\tmost\tother\tsome\tsuch\tno\tnor\tnot" +
			"\tonly\town\tsame\tso\tthan\ttoo\tvery\ts\tt\tcan\twill\tjust\tdon\tshould\tnow";


		// create hash table
		String [] words = stopWords.split("\t");
		for(int i = 0; i < words.length; i++) {
			stopWordsHash.put(words[i], 1);
			//System.out.println("words[i] = " + words[i]);
		}
	}

	private static int getWordIndex(String paragraph, String word){
		int firstWordIndex = -1;
		String [] words = paragraph.split(" ");

		for(int i = 0; i < words.length; i++) {
			if (isStopWordOrMark(words[i].toLowerCase()) != -1){
				continue;
			}
			if(words[i].trim().equals(word.trim())){
				return i;
			}
		}
		return -1;
	}

	private static int isStopWordOrMark(String word){
		if (stopWordsHash.containsKey(word)) {
			return stopWordsHash.get(word);
		}
		return -1;
	}

}
