
log="../performance-measures/results-$1.txt"
date >> $log
echo >> $log

for opts in '' '--disjoint' '--libsvm' '--libsvm --disjoint'; do
	cmd="./scripts/quick-run.sh $1 $opts"
	echo $cmd
	echo $cmd >> $log
	tm=../models/time.txt
	/usr/bin/time -f "%U" -o $tm $cmd
	echo Time: `cat $tm`s >> $log
	cat ../models/accuracy.txt >> $log
	echo >> $log
done

echo "Majority class: " >> $log
./scripts/get-majority.sh ../corpora/pan14-author-profiling-test-$1/truth.dat >> $log

