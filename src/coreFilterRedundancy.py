#!/usr/bin/env python3


'''
    genetribe - coreFilterRedundancy.py
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
from math import log

# score count
def score_count ( sim,mina,minb,maxa,maxb,bitscore_out,evalue_raw):
	mina2 = min(mina)
	minb2 = min(minb)
	maxa2 = max(maxa)
	maxb2 = max(maxb)
	similarity = "%.3f" % np.mean(sim)
	evalue = "%.e" % 10**(-np.median(evalue_raw))
	length = "%.0f" % np.mean([(maxa2-mina2),(maxb2-minb2)])
	bitscore = "%.0f" % sum(bitscore_out)
	return [similarity,length,evalue,bitscore]

# Store data to discover multiple pieces of information
def getinfo (inputfile):
	dc_raw = {}
	with open(inputfile) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			KEY = i[0]+'\t'+i[1]
			dc_raw.setdefault(KEY,[]).append(i)
	return dc_raw

# Filter redundant
def Filter_redundant (inputfile):
	
	dc = getinfo(inputfile)
	
	for k,v in dc.items():
		if len(v) == 1: # only have one hits
			print ('\t'.join(v[0]))
		else:
			sim = []
			mina = []
			minb = []
			maxa = []
			maxb = []
			evalue_raw = []
			bitscore_out = []
			for j in range(len(v)):
				info = v[j]
				sim.append(float(info[2]))
				mina.append(float(info[6]))
				minb.append(float(info[8]))
				maxa.append(float(info[7]))
				maxb.append(float(info[9]))
				bitscore_out.append(float(info[2])/100*float(info[11]))
				
				try:
					evalue_raw.append(-log(float(info[10]),10))
				except ValueError:
					evalue_raw.append(100)
			
			info = score_count(sim,mina,minb,maxa,maxb,bitscore_out,evalue_raw)
			
			print (k+'\t'+str(info[0])+'\t'+str(info[1])+'\t0\t0\t1\t'+str(info[1])+'\t1\t'+str(info[1])+'\t'+str(info[2])+'\t'+str(info[3]))


from optparse import OptionParser

def main():
	usage = "Usage: %prog [options]\n" \
		"Description: filter redundant information of blast hits"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="infile",
                  help="input file", metavar="FILE")
	(options, args) = parser.parse_args()
	Filter_redundant(options.infile)

if __name__ == "__main__":
	main()
