#!/usr/bin/env bash

#     genetribe - sameassembly.sh
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

gettime() {
        echo -e `date '+%Y-%m-%d %H:%M:%S ... '`
}

set -e

if [ -z "$1" ]; then
        echo "The arguments is empty!"
        exit 1
fi
#
Usage () {
	echo ""
	echo "Tool:  GeneTribe sameassembly"
        echo "Usage: genetribe sameassembly -l <firstname> -f <secondname> [options]"
	echo ""
        echo "Description:"
        echo "  Homology inference for the same assembly"
        echo ""
	echo "Options:"
        echo "  -h Show this message and exit"
        echo "  -l <string> Prefix name of first assembly"
        echo "  -f <string> Prefix name of second assembly"
	echo ""
	echo "Author: Chen,Yongming; chen_yongming@126.com"
	echo ""
        exit 1
}
while getopts "hl:f:" opt
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
        ?)
                echo "Unknow argument!"
                exit 1
                ;;
        esac
done

logo () {
        echo ""
        echo "   ==============================="
        echo "  ||                             ||"
        echo "  ||         GeneTribe           ||"
        echo "  ||       Version: v1.2.1       ||"
        echo "  ||                             ||"
        echo "   ==============================="
        echo ""
}
logo

echo `gettime`"prepare files..."
not_file=""
if [ ! -f "${aname}.bed" ];then
	not_file=${not_file}" ${aname}.bed"
fi
if [ ! -f "${bname}.bed" ];then
	not_file=${not_file}" ${bname}.bed"
fi
if [ ! -f "${aname}.genelength" ];then
	not_file=${not_file}" ${aname}.genelength"
fi
if [ ! -f "${bname}.genelength" ];then
	not_file=${not_file}" ${bname}.genelength"
fi

if [ "$not_file" != "" ];then
	echo -en "\n[ERROR]:\n\t File cannot be found: "${not_file}"\n"
	exit 1
fi
#
dec=`echo $(dirname $(readlink -f "$0")) | sed 's/src/bin/g'`
rm -rf ./output
mkdir ./output
cd ./output
#

ln -s ../${aname}.bed ./
ln -s ../${bname}.bed ./
ln -s ../${aname}.genelength ./
ln -s ../${bname}.genelength ./
#

echo `gettime`"obtain overlap between genes..."
bedtools intersect -a ${aname}.bed -b ${bname}.bed -sorted -s -wao | \
                gawk -v OFS='\t' '{if($13!=""&&$13!="0"){print $4,$10,$13}}' > ${aname}_${bname}.overlap
bedtools intersect -a ${bname}.bed -b ${aname}.bed -sorted -s -wao | \
                gawk -v OFS='\t' '{if($13!=""&&$13!="0"){print $4,$10,$13}}' > ${bname}_${aname}.overlap
#

echo `gettime`"calculate score..."
${dec}/sameassemblyMatchscore -a ${aname}.genelength -b ${aname}_${bname}.overlap > ${aname}_${bname}.one2many
${dec}/sameassemblyMatchscore -a ${bname}.genelength -b ${bname}_${aname}.overlap > ${bname}_${aname}.one2many

echo `gettime`"generate RBH and SBH tables..."
#
${dec}/RBH -a ${aname}_${bname}.overlap -b ${bname}_${aname}.overlap | cut -f1,2 | sort | uniq > ${aname}_${bname}.RBH
#
${dec}/sameassemblyBestHit -a ${aname}_${bname}.one2many -b ${aname}_${bname}.RBH > ${aname}_${bname}.single_end
${dec}/sameassemblyBestHit -a ${bname}_${aname}.one2many -b ${aname}_${bname}.RBH > ${bname}_${aname}.single_end
#
cat ${aname}_${bname}.RBH | gawk -vOFS='\t' '{print $1,$2,"RBH"}' > ${aname}_${bname}.one2one
cat ${aname}_${bname}.single_end | gawk -vOFS='\t' '{print $1,$2,"SBH"}' >> ${aname}_${bname}.one2one
cat ${aname}_${bname}.RBH | gawk -vOFS='\t' '{print $2,$1,"RBH"}' > ${bname}_${aname}.one2one
cat ${bname}_${aname}.single_end | gawk -vOFS='\t' '{print $1,$2,"SBH"}' >>${bname}_${aname}.one2one
#
mv ${aname}_${bname}.one2one ${bname}_${aname}.one2one ${aname}_${bname}.one2many ${bname}_${aname}.one2many ../
cd ..
rm -rf ./output
echo `gettime`"done!"
