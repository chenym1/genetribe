#!/usr/bin/env python3

'''
    genetribe - coreScore2one.py
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
import numpy as np

#
def file2dc(input1,input2):
	dc1 = {}
	with open(input1) as INPUT:
		for i in INPUT:
			i = i.strip().split('\t')
			dc1[i[0]+'\t'+i[1]] = '\t'.join([i[2],i[3],i[4]])
		#
	#
	dc2 = {}
	with open(input2) as INPUT:
		for i in INPUT:
			i = i.strip().split('\t')
			dc2[i[1]+'\t'+i[0]] = '\t'.join([i[2],i[3],i[4]])
	return dc1,dc2
#
# combine and unique key
def combine_unique(dc1,dc2):
	keys_raw = list(dc1.keys())+list(dc2.keys())
	keys = list(set(keys_raw))
	#
	for i in range(len(keys)):
		key = keys[i]
		bsr = []
		chromosome = []
		block = []
		if key in dc1 and key in dc2:
			info1 = dc1[key].split('\t')
			info2 = dc2[key].split('\t')
			bsr.append(float(info1[0]))
			bsr.append(float(info2[0]))
			chromosome.append(int(info1[1]))
			chromosome.append(int(info2[1]))
			block.append(float(info1[2]))
			block.append(float(info2[2]))
		elif key in dc1 and not key in dc2:
			info1 = dc1[key].split('\t')
			bsr.append(float(info1[0]))
			chromosome.append(int(info1[1]))
			block.append(float(info1[2]))
		elif key in dc2 and not key in dc1:
			info2 = dc2[key].split('\t')
			bsr.append(float(info2[0]))
			chromosome.append(int(info2[1]))
			block.append(float(info2[2]))
		bsr2 = max(bsr)
		if bsr2 > 1:
			bsr2 = 1
		chromosome2 = chromosome[0]
		block = np.mean(block)
		print (key+'\t'+str(bsr2)+'\t'+str(chromosome2)+'\t'+str(block))
#
from optparse import OptionParser
def main():
	usage = "Usage: %prog -a input1 -b input2 > output\n" \
		"Description: combine and unique two file"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="input1",
		help="Input file1", metavar="FILE")
	parser.add_option("-b", dest="input2",
		help="Input file2", metavar="FILE")
	(options, args) = parser.parse_args()
	dc1,dc2 = file2dc(options.input1,options.input2)
	combine_unique(dc1,dc2)
#
if __name__ == "__main__":
	main()
