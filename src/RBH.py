#!/usr/bin/env python3

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
