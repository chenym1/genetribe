#!/usr/bin/env python3

'''
    genetribe - sameassemblyMatchscore.py
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

def score(lengthfile,input1):
	Adc = {}
	with open(lengthfile) as f:
		for i in f:
			i = i.strip().split('\t')
			Adc[i[0]] = i[1]
		#
	#
	with open(input1) as f:
		for i in f:
			i = i.strip().split('\t')
			length = float(Adc[i[0]])
			overlap = float(i[2])
			score = (overlap/length)*100
			score = '%.2f' % score
			print (i[0]+'\t'+i[1]+'\t'+str(score))
		#
	#
#
from optparse import OptionParser
def main():
	usage = "Usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="lengthfile",
		help="gene length", metavar="FILE")
	parser.add_option("-b", dest="input1",
		help="overlap", metavar="FILE")
	(options, args) = parser.parse_args()
	score(options.lengthfile,options.input1)
#
if __name__ == "__main__":
	main()
