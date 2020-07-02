#!/usr/bin/env python3

'''
    genetribe - corenog-CalculateScore.py
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

import re

# Convert confidence's files to dict
def confidence2dc (confidencd_file):
	typedc = {}
	with open(confidencd_file) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			typedc[i[0]] = i[1]
	return typedc

# Convert bed files to dict
def bed2dc (bed_file):
	beddc = {}
	with open(bed_file) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			beddc[i[3]] = i[0]
	return beddc

# Convert bitscore file to dict:
def bitscore2dc (own_file):
	dc = {}
	with open(own_file) as own:
		for i in own:
			i = i.strip().split('\t')
			if i[0] == i[1]:
				dc[i[0]] = i[11]
	return dc
#
def Filter ( blastfile,beda,bedb,owna,ownb,typea,typeb,stat_confidence) :
	## type dict
	if stat_confidence:
		typeadc = confidence2dc(typea)
		typebdc = confidence2dc(typeb)
	## bitscore into dict
	adc = bitscore2dc(owna)
	bdc = bitscore2dc(ownb)
	## get score
	'''
	filter similarity of pairs
	'''
	with open(blastfile) as blast:
		for i in blast:
			i = i.strip().split('\t')
			geneA = i[0]
			geneB = i[1]
			if geneA != geneB:
				#=======   BSR   ================
				bitscore = i[11]
				try:
					bitAB = float(bdc[geneB])
					bitOb = float(bitscore)/float(bitAB)
				except KeyError:
					try:
						bitAB = float(adc[geneA])
						bitOb = float(bitscore)/float(bitAB)
					except KeyError:
						continue
				#
				chromosome_group = 0
				#======  confidance  =======
				if stat_confidence:
					try:
						type_1 = typeadc[geneA]
						type_2 = typebdc[geneB]
					except KeyError:
                       	                	continue
					if type_1 == "HC" and type_2 == "HC":
						confidence = 0
					elif type_1 == "LC" and type_2 == "LC":
						confidence = 2
					else:
						confidence = 1
				else:
					confidence = 0
				##
				bitOb = '%.3f' % bitOb
				gene_score = chromosome_group+confidence
				print (geneA+'\t'+geneB+'\t'+str(bitOb)+'\t'+str(gene_score))

####
from optparse import OptionParser
def main():
	usage = "Usage: %prog -i \n" \
		"Author: Chen,Yongming; chen_ym@cau.edu.cn; 2020-7-2\n" \
		"Description: Get BSR and chromosome-group score of every hits (nog)."
	parser = OptionParser(usage)
	parser.add_option("-i", dest="blastfile",
                  help="A blast B file", metavar="FILE")
	parser.add_option("-a", dest="beda",
                  help="bed of A genome", metavar="FILE")
	parser.add_option("-b", dest="bedb",
                  help="bed of B genome", metavar="FILE")
	parser.add_option("--oa", dest="owna",
                  help="self-blast of A genome", metavar="FILE")
	parser.add_option("--ob", dest="ownb",
                  help="self-blast of B genome", metavar="FILE")
	parser.add_option("--ta", dest="typea",
                  help="confidence type of A genome", metavar="FILE")
	parser.add_option("--tb", dest="typeb",
                  help="confidence type of B genome", metavar="FILE")
	parser.add_option("-c", action="store_true",  dest = "stat_confidence",
	        help="Whether to count confidence score [default: %default]",default = False, metavar="boolean")
	
	(options, args) = parser.parse_args()
	Filter(options.blastfile,options.beda,options.bedb,options.owna,options.ownb,options.typea,options.typeb,options.stat_confidence)
###
if __name__ == "__main__":
	main()
