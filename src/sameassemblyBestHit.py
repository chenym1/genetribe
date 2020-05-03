#!/usr/bin/env python3
from math import log
#
def cal(datafile,RBHfile):
	data = open(datafile)
	BBH = open(RBHfile)
	BBHdc = {}
	for i in BBH:
		i = i.strip().split('\t')
		if i[0] not in BBHdc:
			BBHdc[i[0]] = ''
		if i[1] not in BBHdc:
			BBHdc[i[1]] = ''
	dc = {}
	for i in data:
		i = i.strip().split('\t')
		value = float(i[2])
		if i[0] not in BBHdc:
			if not i[0] in dc:
				dc[i[0]] = {value:i[1]}
			else:
				dc[i[0]][value] = i[1]
	##
	for i,j in dc.items():
		MAX = max(j.keys())
		gene = j[MAX]
		print (str(i)+'\t'+str(gene))
	#
#
from optparse import OptionParser
def main():
	usage = "Usage: %prog -a scorefile -b RBHfile > output"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="scorefile",
		help="score file", metavar="FILE")
	parser.add_option("-b", dest="RBHfile",
		help="RBH file", metavar="FILE")
	(options, args) = parser.parse_args()
	cal(options.scorefile,options.RBHfile)
#
if __name__ == "__main__":
	main()
