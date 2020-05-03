#!/usr/bin/env python3

'''
    genetribe - corermTwoType.py
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

def final(data):
	dc = {}
	with open(data) as FILE:
		# remove gene pair that have mutual-best and its-best
		for i in FILE:
			i = i.strip().split('\t')
			key = i[0]+'\t'+i[1]
			if not key in dc:
				dc[key] = [i[2],i[3]]
			else:
				dc[key] = ['RBH',i[3]]
	#
	for key,info in dc.items():
		print (key+'\t'+info[0]+'\t'+info[1])
#

from optparse import OptionParser
def main():
	usage = "Usage: %prog -i inputfile\n" \
        	"Description: remove gene pair that have mutual-best and its-best"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="inputfile",
                  help="Input file", metavar="FILE")
	(options, args) = parser.parse_args()
	final(options.inputfile)
#
if __name__ == "__main__":
	main()
