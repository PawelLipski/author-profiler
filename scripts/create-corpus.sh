
N=$1 
T=$2

mkdir ../corpora/pan14-author-profiling-training-$N
mkdir ../corpora/pan14-author-profiling-test-$N

SRC=../corpora/pan14-author-profiling-training-corpus-2014-02-24/pan14-author-profiling-training-corpus-$T-2014-02-24/en/ 
NSRC=`ls -1 $SRC | wc -l`
./scripts/random-copy.sh $SRC ../corpora/pan14-author-profiling-training-$N/ $NSRC $N
./scripts/random-copy.sh $SRC ../corpora/pan14-author-profiling-test-$N/ $NSRC $N ../corpora/pan14-author-profiling-training-$N/

./scripts/make-truth.sh ../corpora/pan14-author-profiling-test-$N/

less ../corpora/pan14-author-profiling-test-$N/truth.dat

