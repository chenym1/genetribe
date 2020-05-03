#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd
#
def weight (inputfile,colinearity_percent,filterscore):
	colinearity_percent = float(colinearity_percent)
	BSR_percent = 100-colinearity_percent
	# filter score
	score_threshold = BSR_percent * float(filterscore)/100
	with open(inputfile) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			BSR = float(i[2])*BSR_percent
			chromosome_group = float(i[3])
			colinearity = float(i[4])*colinearity_percent
			score = (BSR+colinearity) * ((100-chromosome_group)/100)
			if score >= score_threshold:
				score = '%.2f' % score
				print (i[0]+'\t'+i[1]+'\t'+str(score))

from optparse import OptionParser
def main():
	usage = "Usage: %prog -i inputfile -a colinearity_percent -f filterscore > output\n" \
	"Description: weighted score"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="inputfile",
                  help="Input file", metavar="FILE")
	parser.add_option("-a", dest="colinearity_percent",default='50',
                  help="the weight of colinearity score [default: %default]", metavar="FLOAT")
	parser.add_option("-f", dest="filterscore",default='75',
		  help="percent of filtered score [default: %default]", metavar="FLOAT")
	(options, args) = parser.parse_args()
	weight(options.inputfile,options.colinearity_percent,options.filterscore)
#
if __name__ == "__main__":
        main()
