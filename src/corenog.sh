#!/usr/bin/env bash

#     genetribe - corenog.sh
#     Copyright (C) Yongming Chen
#     Contact: chen_yongming@126.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

set -e

if [ -z "$1" ]; then
        echo "The arguments is empty!"
        exit 1
fi

gettime() {
	echo -e `date '+%Y-%m-%d %H:%M:%S ... '`
}

stat_confidence=""

Usage () {
	echo ""
	echo "Tool:   GeneTribe corenog"
        echo "Usage:  genetribe corenog -l <FirstName> -f <SecondName> [options]"
	echo ""
        echo "Description:"
        echo "  Workflow not grouping chromosomes"
        echo ""
	echo "Options:"
        echo "  -h         Show this message and exit"
        echo "  -l <str>   Prefix name of first file"
        echo "  -f <str>   Prefix name of second file"
	echo "  -d <dir>   Pre-computed BLAST file in <dir> [default ./]"
	echo "  -c         Calculate confidence score [default False]"
	echo "  -s <str>   The string for spliting gene from transcript ID [default .]"
	echo "  -e         E-value of BLASTP [default 1e-5]"
	echo "  -n <int>   Number of threads for blast [default 36]"
	echo "  -b <float> Threshold based on BSR for filtering Match Score(0-100) [default 75]"
	echo ""
	echo "Author: Chen,Yongming; chen_yongming@126.com"
	echo ""
	exit 1
}
while getopts "hl:f:d:cs:e:n:b:" opt
do
    case $opt in
        h)
                Usage
                exit 1
                ;;
        l)
                aname=$OPTARG
                ;;
        f)
                bname=$OPTARG
                ;;
	d)
		directory=$OPTARG
		;;
	c)
		stat_confidence="-c"
		;;
	s)
		fa_str=$OPTARG
		;;
	e)
		evalue=$OPTARG
		;;
	n)
		num_threads=$OPTARG
		;;
	b)
		score_threshold=$OPTARG
		;;
        ?)
                echo "Unknow argument!"
                exit 1
                ;;
        esac
done

dec=`echo $(dirname $(readlink -f "$0")) | sed 's/src/bin/g'`

logo () {
        echo ""
        echo "   ==============================="
        echo "  ||                             ||"
        echo "  ||         GeneTribe           ||"
        echo "  ||       Version: v1.1.0       ||"
        echo "  ||                             ||"
        echo "   ==============================="
        echo ""
}
logo
 
echo `gettime`"prepare files..."

${dec}/corenog-detectFileExist \
	-d ${directory-./} \
	-a ${aname} \
	-b ${bname} \
	-e ${evalue-1e-5} \
	-n ${num_threads-36} \
	-f ${fa_str-.} \

${dec}/corenog-lns \
	-a ${aname} \
	-b ${bname}

cd ./output

if [ "$aname"x = "$bname"x ];then
	bname=${aname}itself
fi
#===
echo `gettime`"calculate BSR, CBS and Penalty..."

for key in ${aname}__${bname} ${bname}__${aname};do

	array=(${key//__/ })
        array=${array[@]}
        key1=`echo $array | gawk '{print $1}'`
        key2=`echo $array | gawk '{print $2}'`

	${dec}/corenog-CalculateScore \
                -i ${key}.blast2 \
                -a ${key1}.bed \
                -b ${key2}.bed \
                --oa ${key1}_${key1}.blast2 \
                --ob ${key2}_${key2}.blast2 \
		${stat_confidence} > ${key}.score1

	echo ""
	python -m jcvi.compara.catalog ortholog ${key1} ${key2}
	echo ""

	${dec}/coreCBS -i ${key1}.${key2}.lifted.anchors -a ${key1}.bed -b ${key2}.bed -o ${key}

	${dec}/coreMergeScore -i ${key}.score1 -c ${key}.block_pos -a ${key1}.bed -b ${key2}.bed > ${key}.score2

done

#===
${dec}/coreScore2one -a ${aname}_${bname}.score2 -b ${bname}_${aname}.score2 > ${aname}_${bname}.score

cat ${aname}_${bname}.score | gawk -vOFS='\t' '{print $2,$1,$3,$4,$5}' > ${bname}_${aname}.score

#===
echo `gettime`"evaluate optimal α for weighting score..."

for value in 0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 99;do

	${dec}/coreSetWeight -i ${aname}_${bname}.score -a ${value} -f ${score_threshold-75} \
		> ${aname}_${bname}_chr11xchr22.weighted_score

	${dec}/coreSetWeight -i ${bname}_${aname}.score -a ${value} -f ${score_threshold-75} \
		> ${bname}_${aname}_chr22xchr11.weighted_score

	totalnum=`cat ${aname}.bed | wc -l`

	${dec}/RBH -a ${aname}_${bname}_chr11xchr22.weighted_score -b ${bname}_${aname}_chr22xchr11.weighted_score \
		> ${aname}_${bname}_chr11xchr22.BMP

	wc -l ${aname}_${bname}_chr11xchr22.BMP | \
		cut -d" " -f1 | gawk -v bmpvalue=${value} -v total=${totalnum} -vOFS='\t' '{print bmpvalue,$1/total,$1,total}' >> ${aname}_${bname}_chr11xchr22.stat

done

max_percent=`sort -k2nr ${aname}_${bname}_chr11xchr22.stat | sed -n '1p' | cut -f1`

echo `gettime`"α = "${max_percent}"..."
echo `gettime`"merge original score..."

#===
${dec}/coreSetWeight -i ${aname}_${bname}.score \
        -a ${max_percent} \
	-f ${score_threshold-75} \
	> ${aname}_${bname}.weighted_score

${dec}/coreSetWeight -i ${bname}_${aname}.score \
        -a ${max_percent} \
	-f ${score_threshold-75} \
	> ${bname}_${aname}.weighted_score


#===
echo `gettime`"process all chromosome pairs..."

${dec}/RBH -a ${aname}_${bname}.weighted_score -b ${bname}_${aname}.weighted_score \
	> ${aname}_${bname}.BMP

${dec}/coreSingleSideBest -a ${aname}_${bname}.weighted_score \
	-b ${aname}_${bname}.BMP \
	> ${aname}_${bname}.single_end

#
cat ${aname}_${bname}.BMP | \
	gawk -vOFS='\t' '{print $2,$1}' > ${bname}_${aname}.BMP

${dec}/coreSingleSideBest -a ${bname}_${aname}.weighted_score \
	-b ${bname}_${aname}.BMP \
	> ${bname}_${aname}.single_end

#===
echo `gettime`"merged results..."

for key in ${aname}_${bname} ${bname}_${aname};do

	array=(${key//_/ })
	array=${array[@]}
	key1=`echo $array | gawk '{print $1}'`
	key2=`echo $array | gawk '{print $2}'`

	cat ${key}.BMP | gawk -vOFS='\t' '{print $1,$2,"RBH"}' > ${key}.total
	cat ${key}.single_end | gawk -vOFS='\t' '{print $1,$2,"SBH"}' >> ${key}.total

	${dec}/coreSingleton -a ${key1}.bed -b ${key}.total > ${key}.singleton

done

#===

mv ${aname}_${bname}.weighted_score ../${aname}_${bname}.one2many
mv ${bname}_${aname}.weighted_score ../${bname}_${aname}.one2many
mv ${aname}_${bname}.total ../${aname}_${bname}.one2one
mv ${bname}_${aname}.total ../${bname}_${aname}.one2one
mv ${aname}_${bname}.singleton ../
mv ${bname}_${aname}.singleton ../
cd ..

cat ${aname}_${bname}.one2one | gawk -vOFS="\t" '{if($3=="RBH")print}' > ${aname}_${bname}.RBH
cat ${aname}_${bname}.one2one | gawk -vOFS="\t" '{if($3=="SBH")print}' > ${aname}_${bname}.SBH
cat ${bname}_${aname}.one2one | gawk -vOFS="\t" '{if($3=="SBH")print}' > ${bname}_${aname}.SBH

rm -rf output
echo `gettime`"done!"
