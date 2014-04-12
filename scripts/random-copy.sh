
all=$3
todo=$4

for f in $1/*; do
	if [ $[RANDOM % all < todo] -ne 0 ]; then
		cp -v $f $2
		todo=$[todo - 1]
	fi
	all=$[all - 1]
done

