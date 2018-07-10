echo "Lookup results: $i"
/usr/local/hadoop/bin/hadoop fs -cat wordcount/output/$1/* | sort -n -k2 -r | head -n7
