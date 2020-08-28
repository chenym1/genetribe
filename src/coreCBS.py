#!/usr/bin/env python3

'''
    genetribe - coreCBS.py
    Copyright (C) Yongming Chen
    Contact: chen_yongming@126.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
'''


import sys
import math
import pandas as pd
import numpy as np

# store block information to dict
def block2dc ( block_file ):
	dc = {}
	key_num = 0
	with open(block_file) as block:
		for i in block:
			if i.startswith('##'):
				key_num = key_num + 1
			else:
				dc.setdefault(key_num,[]).append(i.strip())
			if (key_num % 2) == 0:
				key_num = key_num + 1

	# block_dc to genelist
	pair_dc = {}
	block_dc = {}
	for i in dc.keys():
		info = dc[i]
		gene_num = len(info)
		gene_list1 = []
		gene_list2 = []
		pair_info = []
		for j in range(gene_num):
			pair = info[j].split('\t')
			if pair[0] not in gene_list1:
				gene_list1.append(pair[0])
			if pair[1] not in gene_list2:
				gene_list2.append(pair[1])
			pair_info.append(','.join([pair[0],pair[1]]))
		pair_dc[i] = pair_info
		block_dc[i] = [gene_list1,gene_list2]	
	return (dc,pair_dc,block_dc)

# bedfile to pandas
def bed2pd ( bed_file ):
	bedtmp = pd.read_csv(bed_file,sep="\t",header=None)
	bedtmp.columns = ["chr","start","end","id","score","strand"]
	nrow = bedtmp.shape[0]
	bedtmp.index = range(nrow)
	return bedtmp

# get block information , including chromosome,start,end and genenum
def getinfo(bed1tmp,gene_list1):
	info = bed1tmp[bed1tmp["id"].isin(gene_list1)]
	geneA_loc = info.index.tolist()
	gene_num = float(max(geneA_loc)-min(geneA_loc)+1)
	CHR = info['chr'].values.tolist()[0]
	POS = info['start'].values.tolist() + info['end'].values.tolist()
	MIN = min(POS)
	MAX = max(POS)
	return [[CHR,MIN,MAX],gene_num]

# get median
def count_median(block_dc,bed1tmp,bed2tmp):
	score_info = []
	for i in block_dc.keys():
		gene_list1 = block_dc[i][0]
		gene_list2 = block_dc[i][1]
		infoA = getinfo(bed1tmp,gene_list1)
		infoB = getinfo(bed2tmp,gene_list2)
		gene_num = int(infoA[1])+int(infoB[1])
		score_info.append(gene_num)
	return np.median(score_info)

# final step
def final(block_dc,pair_dc,bed1tmp,bed2tmp,outname):
	out1 = open(outname+'.colinearity_info','w')
	out2 = open(outname+'.block_pos','w')
	block_num = 1
	median = count_median(block_dc,bed1tmp,bed2tmp)
	out1.write("## median:"+str(median)+'\n')
	for i in block_dc.keys():
		gene_list1 = block_dc[i][0]
		gene_list2 = block_dc[i][1]
		infoA = getinfo(bed1tmp,gene_list1)
		infoB = getinfo(bed2tmp,gene_list2)
		count = int(infoA[1])+int(infoB[1])
		name_id = 'block_'+str(block_num)
		pair = '; '.join(pair_dc[i])
		pos = str(infoA[0][0])+':'+str(infoA[0][1])+'-'+str(infoA[0][2])+',' \
			+str(infoB[0][0])+':'+str(infoB[0][1])+'-'+str(infoB[0][2])
		score = "%.3f" % ( count / (count+median) )
		ratio = (float(len(gene_list1))*infoB[1]+float(len(gene_list2))*infoA[1])/(2*infoA[1]*infoB[1])
		out1.write('\t'.join([name_id,pos,str(count),str(ratio),str(score),pair])+'\n')
		out2.write('\t'.join([str(infoA[0][0]),str(infoA[0][1]),str(infoA[0][2]),str(infoB[0][0]),str(infoB[0][1]),str(infoB[0][2]),str(score)])+'\n')
		block_num += 1

#
from optparse import OptionParser
def main():
	usage = "Usage: %prog -i input.anchors -a bed1 -b bed2 > outputfile\n" \
            "Description: Calculate Collinearity Block Score (CBS) from the result of MCscan"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="block_file",
                  help="The block anchors file obtaining from MCScan", metavar="FILE")
	parser.add_option("-a", dest="bed1",
		help="First bed", metavar="FILE")
	parser.add_option("-b", dest="bed2",
                help="Second bed", metavar="FILE")
	parser.add_option("-o", dest="outname",
                help="prefix name of output file", metavar="STR")
	(options, args) = parser.parse_args()
	(dc,pair_dc,block_dc) = block2dc(options.block_file)
	bed1tmp = bed2pd(options.bed1)
	bed2tmp = bed2pd(options.bed2)
	final(block_dc,pair_dc,bed1tmp,bed2tmp,options.outname)

#
if __name__ == "__main__":
	main()
