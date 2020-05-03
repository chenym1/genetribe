#!/usr/bin/env python3

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
