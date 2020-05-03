#!/usr/bin/env python3
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
            "Description: Extract the longest protein sequence from protein fasta"
    parser = OptionParser(usage)
    parser.add_option("-i", dest="infile",
                  help="Input file", metavar="FILE")
    parser.add_option("-s", dest="strsplit",default='.',
                  help="the string of split geneid from transcript ID", metavar="STR")
    (options, args) = parser.parse_args()
    longestfasta (options.infile,options.strsplit)


# ===========================================
if __name__ == "__main__":
    main()
