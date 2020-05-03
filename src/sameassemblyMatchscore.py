#!/usr/bin/env python3
#
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
	usage = "Usage: %prog -a genelengthfile -b inputfile > output"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="lengthfile",
		help="gene length file", metavar="FILE")
	parser.add_option("-b", dest="input1",
		help="overlap file", metavar="FILE")
	(options, args) = parser.parse_args()
	score(options.lengthfile,options.input1)
#
if __name__ == "__main__":
	main()
