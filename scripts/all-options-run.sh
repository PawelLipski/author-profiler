
for opts in '' '--disjoint' '--liblinear' '--liblinear --disjoint'; do
	cmd="./scripts/quick-run.sh $1 $opts"
	echo $cmd
	log="../performance-measures/results-$1.txt"
	echo $cmd >> $log
	tm=../models/time.txt
	/usr/bin/time -f "%U" -o $tm $cmd
	cat $tm >> $log
	cat ../models/accuracy.txt >> $log
	echo >> $log
done

