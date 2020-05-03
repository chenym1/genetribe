#!/usr/bin/env python3

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
	#
	dc = getinfo(inputfile)
	#
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
				#
				try:
					evalue_raw.append(-log(float(info[10]),10))
				except ValueError:
					evalue_raw.append(100)
			#
			info = score_count(sim,mina,minb,maxa,maxb,bitscore_out,evalue_raw)
			#
			print (k+'\t'+str(info[0])+'\t'+str(info[1])+'\t0\t0\t1\t'+str(info[1])+'\t1\t'+str(info[1])+'\t'+str(info[2])+'\t'+str(info[3]))

#

from optparse import OptionParser

def main():
	usage = "Usage: %prog -i input.blast > outputfile\n" \
		"Filter blast-result's redundant information\n" \
		"Print to stdout"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="infile",
                  help="Input file", metavar="FILE")
	(options, args) = parser.parse_args()
	Filter_redundant(options.infile)

#
if __name__ == "__main__":
	main()
