#!/usr/bin/env python3

'''
    genetribe - coreSingleSideBest.py
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

from math import log
#
def find_single (score,RBH):
	data = open(score)
	BMP = open(RBH)
	BMPdc = {}
	for i in BMP:
		i = i.split('\t')
		if i[0] not in BMPdc:
			BMPdc[i[0]] = ''
		#
	#
	dc = {}
	for i in data:
		i = i.strip().split('\t')
		value = float(i[2])
		if i[0] not in BMPdc:
			if not i[0] in dc:
				dc[i[0]] = {value:i[1]}
			else:
				dc[i[0]][value] = i[1]
			#
		#
	#
	for i,j in dc.items():
		MAX = max(j.keys())
		gene = j[MAX]
		print (str(i)+'\t'+str(gene))
	#
from optparse import OptionParser
def main():
	usage = "Usage: %prog [options]\n" \
	"Description: find single-side best hits (SBH)"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="score",
		help="weight score", metavar="FILE")
	parser.add_option("-b", dest="RBH",
		help="RBH", metavar="FILE")
	(options, args) = parser.parse_args()
	find_single(options.score,options.RBH)
#
if __name__ == "__main__":
        main()
