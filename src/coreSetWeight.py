#!/usr/bin/env python3

'''
    genetribe - coreSetWeight.py
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
	usage = "Usage: %prog [options]\n" \
	"Description: weight score"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="inputfile",
		help="input file", metavar="FILE")
	parser.add_option("-a", dest="colinearity_percent",default='50',
		help="weight of colinearity score [default: %default]", metavar="FLOAT")
	parser.add_option("-f", dest="filterscore",default='75',
		help="percent of filtered score [default: %default]", metavar="FLOAT")
	(options, args) = parser.parse_args()
	weight(options.inputfile,options.colinearity_percent,options.filterscore)
#
if __name__ == "__main__":
	main()
