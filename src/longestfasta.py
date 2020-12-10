#!/usr/bin/env python3

'''
    genetribe - longestfasta.py
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
def longestfasta( infile,strsp):
	dc = {}
	#
	with open(infile) as fa:
		for line in fa:
			if line.startswith('>'):
				ID = line
				dc[ID] = ''
			else:
				dc[ID] += line
	#
	max_dc = {}
	for i,j in dc.items():
		info = i.split(' ')
		if 'gene:' in i:
			for num in range(len(info)):
				tmp_str = info[num]
				if tmp_str.startswith('gene:'):
					gene = '>'+tmp_str.split('gene:')[1]
		else:
			gene = info[0].split(strsp)
			if len(gene) > 1:
				gene = strsp.join(gene[:len(gene)-1])
			else:
				gene = gene[0]
		#
		if not gene in max_dc:
			max_dc[gene] = j
		else:
			length = len(j)
			if length > len(max_dc[gene]):
				max_dc[gene] = j
	#
	for i,j in max_dc.items():
		print (i.strip())
		print (j.strip())
#
from optparse import OptionParser
# ===========================================
def main():
    usage = "Usage: %prog -i pep.fa -s strsplit\n" \
            "Description: extract longest protein sequence from protein fasta"
    parser = OptionParser(usage)
    parser.add_option("-i", dest="infile",
                  help="input file", metavar="FILE")
    parser.add_option("-s", dest="strsplit",default='.',
                  help="the string for spliting gene from transcript ID", metavar="STR")
    (options, args) = parser.parse_args()
    longestfasta (options.infile,options.strsplit)


# ===========================================
if __name__ == "__main__":
    main()
