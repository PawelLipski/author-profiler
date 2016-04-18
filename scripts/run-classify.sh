
python classify.py ../corpora/pan13-author-profiling-test-$1/

exit

I=0
for f in ../corpora/pan13-author-profiling-test-$1/*; do 
  I=$[I+1]
  #echo "Classify $I/$1" >&2
  python classify.py $f; 
done

