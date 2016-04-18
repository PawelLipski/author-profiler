
run() {
	N=$1
	shift
	if [ $# -ne 0 ]; then
		echo Training for $@...
		./scripts/run-train.sh $N $@ #> /dev/null
		echo Classifying for $@...
		./scripts/run-classify.sh $N 
		#| grep SAME | wc -l`/$N classified properly
	fi
}

for a in '' FW; do
		for c in '' CNG; do
			for d in '' CW; do
				run $1 $a $c $d
			done
		done
done

