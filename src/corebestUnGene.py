#!/usr/bin/env python3

import sys
import re
#
def correct ( rawfile , totalchr , score , bed) :
	with open(totalchr) as TOTALCHR:
		TOTALCHR1 = TOTALCHR.readline()
		TOTALCHR1 = TOTALCHR1.strip().split('\t')
		rawCHR = TOTALCHR1[0]
	#
	beddc = {}
	with open(bed) as bed2:
		for i in bed2:
			i = i.strip().split('\t')
			beddc[i[3]] = i[0]
		#
	score_dc = {}
	with open(score) as score2:
		for i in score2:
			i = i.strip().split('\t')
			score_dc[i[0]+'\t'+i[1]] = i[2]
		#
	undc = {}
	with open(rawfile) as inputfile:
		for i in inputfile:
			i = i.strip().split('\t')
			CHR = re.sub('[0-9][0-9]|[0-9]','N',beddc[i[0]])
			if re.match(rawCHR,CHR):
				print ('\t'.join(i))
				 #continue
			else:
				if not i[0] in undc:
					undc[i[0]] = {i[3]:[[i[1],i[2]]]}
				else:
					if not i[3] in undc[i[0]]:
						undc[i[0]][i[3]] = [[i[1],i[2]]]
					else:
						undc[i[0]][i[3]].append([i[1],i[2]])
	#
	for i in undc.keys():
		pair_dc = undc[i]
		for pair in pair_dc.keys():
			pair_info = pair_dc[pair]
			score = float(0)
			gene = ''
			group = ''
			for kk in range(len(pair_info)):
				info = pair_info[kk]
				try:
					if float(score_dc[i+'\t'+info[0]]) >= score:
						score = float(score_dc[i+'\t'+info[0]])
						gene = info[0]
						group = info[1]
				except KeyError:
					gene = info[0]
					group = info[1]
			print (i+'\t'+gene+'\t'+group+'\t'+pair)
#
from optparse import OptionParser
# ===========================================
def main():
	usage = "Usage: %prog -i rawfile -t totalchr -b bed\n" \
            "Description: get best pair of Unknown chromosome gene"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="rawfile",
                  help="Input total file", metavar="FILE")
	parser.add_option("-t", dest="totalchr",
                  help="total chromosome", metavar="FILE")
	parser.add_option("-c", dest="score",
                  help="score file", metavar="FILE")
	parser.add_option("-b", dest="bed",
                  help="bed file", metavar="FILE")
	(options, args) = parser.parse_args()

	correct (options.rawfile,options.totalchr,options.score,options.bed)
# ===========================================
if __name__ == "__main__":
	main()
