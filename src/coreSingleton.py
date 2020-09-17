#!/usr/bin/env python3

'''
    genetribe - coreSingleton.py
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

def gene2list(one2onefile):
	dc = {}
	with open(one2onefile) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			dc[i[0]] = ''
		#
	#
	return dc

def singleton(bedfile,one2onefile):
	genedc = gene2list(one2onefile)
	with open(bedfile) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			if i[3] not in genedc:
				print (i[3])

from optparse import OptionParser
def main():
	usage = "Usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="bedfile",
		help="bed", metavar="FILE")
	parser.add_option("-b", dest="one2onefile",
		help="one2one", metavar="FILE")
	(options, args) = parser.parse_args()
	singleton(options.bedfile,options.one2onefile)

if __name__ == "__main__":
	main()
