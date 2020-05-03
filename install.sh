#!/usr/bin/env sh

stat=0

echo "check software dependencies"

if [ `which blastp | wc -l` == 0 ];then
	echo 'ERROR: blast cannot be found'
	stat=$((stat+1))
fi

if [ `which bedtools | wc -l` == 0 ];then
	echo 'ERROR: bedtools cannot be found'
	stat=$((stat+1))
fi

python3 -m jcvi.compara 2>jcvi.s
if [ `cat jcvi.s | wc -l` == 1 ];then
	echo 'ERROR: jcvi (MCscan) cannot be found'
	stat=$((stat+1))
fi
rm jcvi.s

if [ $stat != 0 ];then
	exit 1
fi

rm -rf bin/
mkdir bin/
cd bin/
	for ph in ../src/*py ../src/*sh;do
		pc=`basename $ph | cut -d"." -f1`
		echo "bulding "`basename $ph`
		ln -s $ph $pc
		chmod +x $pc
	done
cd ..

echo ""
echo "Installation in finished"
echo ""
echo "Please add the following line to your ~/.bash_profile, and source ~/.bash_profile before running genetribe."
echo ""
echo '	export PATH='`pwd`':$PATH'
echo ""
