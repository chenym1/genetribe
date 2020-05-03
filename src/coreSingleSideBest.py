#!/usr/bin/env python3
'''
python single_end_best.py aname_bname_firstchrxsecondchr.weighted_score aname_bname_firstchrxsecondchr.BMP > aname_bname_firstchrxsecondchr.single
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
	usage = "Usage: %prog -a score -b RBH\n" \
        "Description: find single-best of genes that not have RBH"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="score",
                  help="the weighted-score file", metavar="FILE")
	parser.add_option("-b", dest="RBH",
                  help="the RBH file", metavar="FILE")
	(options, args) = parser.parse_args()
	find_single(options.score,options.RBH)
#
if __name__ == "__main__":
        main()
