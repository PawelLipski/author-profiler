
cat $1 | cut -f 4,7 -d: | sort | uniq -c | sort -n -r | head -1 

