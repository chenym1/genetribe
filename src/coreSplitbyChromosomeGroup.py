#!/usr/bin/env python3

'''
    genetribe - coreSplitbyChromosomeGroup.py
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

def Filter (blastfile,beda,bedb,matchpair,totalchr):
	# match pair
	matchpair = matchpair.split(',')
	matchA = matchpair[0]
	matchB = matchpair[1]
	## totalchr
	with open(totalchr) as TOTALCHR:
		TOTALCHR1 = TOTALCHR.readline()
		TOTALCHR1 = TOTALCHR1.strip().split('\t')
		totalchrlist = [TOTALCHR1[0],TOTALCHR1[1]]
	## A chr pos
	with open(beda) as ainfo:
		adc = {}
		for i in ainfo:
			i = i.strip().split('\t')
			gene = i[3]
			CHR = i[0]
			if gene not in adc:
				adc[gene] = CHR
	### B chr pos
	with open(bedb) as binfo:
		bdc = {}
		for i in binfo:
			i = i.strip().split('\t')
			gene = i[3]
			CHR = i[0]
			if gene not in bdc:
				bdc[gene] = CHR
	###
	with open(blastfile) as blast:
		for i in blast:
			try:
				i = i.strip().split('\t')
				chra1 = adc[i[0]]
				chrb1 = bdc[i[1]]
				chra = re.sub('[0-9][0-9]|[0-9]','N',chra1)
				chrb = re.sub('[0-9][0-9]|[0-9]','N',chrb1)
				if re.search(matchA,chra) and re.search(matchB,chrb):
					#if re.search(matchA,chra).group()[A_num_index] == re.search(matchB,chrb).group()[B_num_index]:
					print ('\t'.join(i))
				elif re.search(matchA,chra) and ( not re.search(totalchrlist[1],chrb) ):
					print ('\t'.join(i))
				elif ( not re.search(totalchrlist[0],chra) ) and re.search(matchB,chrb):
					print ('\t'.join(i))
				elif ( not re.search(totalchrlist[0],chra)) and ( not re.search(totalchrlist[1],chrb) ):
					print ('\t'.join(i))
			except KeyError:
				continue
###
from optparse import OptionParser
def main():
	usage = "Usage: %prog -i blast_A_to_B -l A.bed -f B.bed -m chrNA,TuN\n" \
                "Description: Match hit by same chromosome"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="blastfile",
                  help="blast file of A to B", metavar="FILE")
	parser.add_option("-l", dest="beda",
                  help="A.bed", metavar="FILE")
	parser.add_option("-f", dest="bedb",
                  help="B.bed", metavar="FILE")
	parser.add_option("-m", dest="matchpair",
                  help="chrNA,TuN", metavar="FILE")
	parser.add_option("-t", dest="totalchr",
                  help="chromosome name and re", metavar="FILE")
	(options, args) = parser.parse_args()
	Filter(options.blastfile,options.beda,options.bedb,options.matchpair,options.totalchr)
###
if __name__ == "__main__":
	main()
