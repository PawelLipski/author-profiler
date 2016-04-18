
from=$1
to=$2

all=$3
todo=$4

excl=$5

for f in $from/*; do
	if [ $[RANDOM % all < todo] -ne 0 ] && ! [ -f $5/$f ]; then
		cp -v $f $to
		todo=$[todo - 1]
	fi
	all=$[all - 1]
done

