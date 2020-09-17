#!/usr/bin/env python3

'''
    genetribe - coreCorrectTotal.py
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
import re

def correct ( rawfile , totalchr , bed ):
	with open(totalchr) as TOTALCHR:
		TOTALCHR1 = TOTALCHR.readline()
		TOTALCHR1 = TOTALCHR1.strip().split('\t')
		rawCHR = TOTALCHR1[1]
	#
	beddc = {}
	with open(bed) as bed2:
		for i in bed2:
			i = i.strip().split('\t')
			beddc[i[3]] = i[0]
    		#
	with open(rawfile) as inputfile:
		for i in inputfile:
			i = i.strip().split('\t')
			CHR = re.sub('[0-9][0-9]|[0-9]','N',beddc[i[1]])
			if not re.search(rawCHR,CHR):
				i[3] = "unknown"
			print ('\t'.join(i))


from optparse import OptionParser

# ===========================================
def main():
	usage = "Usage: %prog [options]\n" \
   	     "Description: correct one2one file"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="rawfile",
                  help="Input one2one file", metavar="FILE")
	parser.add_option("-t", dest="totalchr",
                  help="all chromosome", metavar="FILE")
	parser.add_option("-b", dest="bed",
                  help="bed 2", metavar="FILE")
	(options, args) = parser.parse_args()

	correct (options.rawfile,options.totalchr,options.bed)
#
if __name__ == "__main__":
	main( )
