
out=$1/truth.dat
rm -f $out
for f in $1/*; do 
	basename $f | sed 's/.xml//' | sed 's/_en_/%/' | sed 's/%\(.*\)_\(.*\)/:::\2:::\1/' >> $out
done

