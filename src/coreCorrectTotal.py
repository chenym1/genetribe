#!/usr/bin/env python3
import sys
import re
#
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
#
from optparse import OptionParser
# ===========================================
def main():
	usage = "Usage: %prog -i rawfile -t totalchr -b bed\n" \
   	     "Description: correct total file"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="rawfile",
                  help="Input total file", metavar="FILE")
	parser.add_option("-t", dest="totalchr",
                  help="total chromosome", metavar="FILE")
	parser.add_option("-b", dest="bed",
                  help="second bed file", metavar="FILE")
	(options, args) = parser.parse_args()

	correct (options.rawfile,options.totalchr,options.bed)
# ===========================================
if __name__ == "__main__":
	main( )
