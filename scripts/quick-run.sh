
./train.py $2 -i ../corpora/pan14-author-profiling-training-$1/ -o ../models/

./classify.py -i ../corpora/pan14-author-profiling-training-$1/ -m ../models/ -o ../classify-outputs/

