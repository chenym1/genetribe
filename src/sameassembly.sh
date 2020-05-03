#!/usr/bin/env bash

set -e

if [ -z "$1" ]; then
        echo "The arguments is empty!"
        exit 1
fi
#
Usage () {
        echo "Usage:"
	echo "  genetribe sameassembly -l <firstname> -f <secondname> -d <dir>"
        echo "Description:"
        echo "  Homolog inference for same assembly"
        echo "Author:Chen,Yongming;2019-3-20
"
        echo "Options:"
        echo "  -h Show this message and exit"
        echo "  -l <string> Prefix name of first assembly"
        echo "  -f <string> Prefix name of second assembly"
        echo "  -d <dir> bed genelength file in <dir>"
        exit 1
}
while getopts "hl:f:d:" opt
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
        ?)
                echo "Unknow argument!"
                exit 1
                ;;
        esac
done

#
not_file=""
if [ ! -f "${directory}/${aname}.bed" ];then
	not_file=${not_file}" ${directory}/${aname}.bed"
fi
if [ ! -f "${directory}/${bname}.bed" ];then
	not_file=${not_file}" ${directory}/${bname}.bed"
fi
if [ ! -f "${directory}/${aname}_geneLength.txt" ];then
	not_file=${not_file}" ${directory}/${aname}_geneLength.txt"
fi
if [ ! -f "${directory}/${bname}_geneLength.txt" ];then
	not_file=${not_file}" ${directory}/${bname}_geneLength.txt"
fi

if [ "$not_file" != "" ];then
	echo -en "\n[ERROR]:\n\t File cannot be found: "${not_file}"\n"
	exit 1
fi
#
rm -rf ./output
mkdir ./output
cd ./output
#
dec=$(dirname $(readlink -f "$0"))

ln -s ${directory}/${aname}.bed ./
ln -s ${directory}/${bname}.bed ./
#

bedtools intersect -a ${aname}.bed -b ${bname}.bed -sorted -wao | \
                gawk -v OFS='\t' '{if($13!=""&&$13!="0"){print $4,$10,$13}}' > ${aname}_${bname}.overlap
bedtools intersect -a ${bname}.bed -b ${aname}.bed -sorted -wao | \
                gawk -v OFS='\t' '{if($13!=""&&$13!="0"){print $4,$10,$13}}' > ${bname}_${aname}.overlap
#
${dec}/sameassemblyMatchscore ${directory}/${aname}_geneLength.txt ${aname}_${bname}.overlap > ${aname}_${bname}.one2many
${dec}/sameassemblyMatchscore ${directory}/${bname}_geneLength.txt ${bname}_${aname}.overlap > ${bname}_${aname}.one2many
#
${dec}/RBH -a ${aname}_${bname}.overlap -b ${bname}_${aname}.overlap | cut -f1,2 | sort | uniq > ${aname}_${bname}.RBH
#
${dec}/sameassemblyBestHit ${aname}_${bname}.one2many ${aname}_${bname}.RBH > ${aname}_${bname}.single_end
${dec}/sameassemblyBestHit ${bname}_${aname}.one2many ${aname}_${bname}.RBH > ${bname}_${aname}.single_end
#
cat ${aname}_${bname}.RBH | gawk -vOFS='\t' '{print $1,$2,"RBH"}' > ${aname}_${bname}.one2one
cat ${aname}_${bname}.single_end | gawk -vOFS='\t' '{print $1,$2,"SBH"}' >> ${aname}_${bname}.one2one
cat ${aname}_${bname}.RBH | gawk -vOFS='\t' '{print $2,$1,"RBH"}' > ${bname}_${aname}.one2one
cat ${bname}_${aname}.single_end | gawk -vOFS='\t' '{print $1,$2,"SBH"}' >>${bname}_${aname}.one2one
#
mv ${aname}_${bname}.one2one ${bname}_${aname}.one2one ${aname}_${bname}.one2many ${bname}_${aname}.one2many ${aname}_${bname}.overlap ${bname}_${aname}.overlap ../
cd ..
rm -rf ./output
