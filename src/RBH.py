#!/usr/bin/env python3

'''
    genetribe - RBH.py
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

def file2dc(FILE):
	dc = {}
	with open(FILE) as FILE2:
		for i in FILE2:
			i = i.strip().split('\t')
			if not i[0] in dc:
				dc[i[0]] = [i[1],float(i[2])]
			else:
				if float(i[2]) > dc[i[0]][1]:
					dc[i[0]] = [i[1],float(i[2])]
				#
			#
		#
	#
	dc_2 = {}
	for i in dc.keys():
		dc_2[i+'\t'+dc[i][0]] = dc[i][1]
	#
	return dc_2

def calculate(blast1,blast2):
	dc1 = file2dc(blast1)
	dc2 = file2dc(blast2)
	for i in dc1.keys():
		key2 = i.split('\t')
		key2 = key2[1]+'\t'+key2[0]
		if key2 in dc2:
			print (i)
		#
	#

from optparse import OptionParser
def main():
	usage = "Usage: %prog -a input1 -b input2 > output\n" \
        "Description: Obtain Reciprocal Best Hits (RBH)\n\n"\
	"Exmaple:\n"\
	" Input1:\n"\
	"	A1	B1	100\n"\
	"	A1	B2	200\n"\
	" Input2\n"\
	"	B1	A1	200\n"\
	"	B2	A1	300\n"\
	" Output:\n"\
	"	A1	B2"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="blast1",
                  help="Input file1", metavar="FILE")
	parser.add_option("-b", dest="blast2",
                  help="Input file2", metavar="FILE")
	(options, args) = parser.parse_args()
	calculate(options.blast1,options.blast2)
#
if __name__ == "__main__":
	main()
