
N=$1
shift

./train.py $@ -i ../corpora/pan14-author-profiling-training-$N/ -o ../models/ && ./classify.py -i ../corpora/pan14-author-profiling-test-$N/ -m ../models/ -o ../classify-outputs/

