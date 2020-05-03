#!/usr/bin/env python3
import re
#
#def getnum ( Chr , chromosome):
#        index = Chr.find('N')
#        chr_suffix = Chr[index+1:]
#        length = len(chr_suffix)
#        chr_match = re.search('[0-9]'+chr_suffix+'|[0-9][0-9]'+chr_suffix,chromosome).group()
#        length = len(chr_match) - length
#        num = chr_match[0:length]
#        return num
#
def Filter (blastfile,beda,bedb,matchpair,totalchr):
	# match pair
	matchpair = matchpair.split(',')
	matchA = matchpair[0]
	matchB = matchpair[1]
	## totalchr
	with open(totalchr) as TOTALCHR:
		TOTALCHR1 = TOTALCHR.readline()
		TOTALCHR1 = TOTALCHR1.strip().split('\t')
		totalchrlist = [TOTALCHR1[0],TOTALCHR1[1]]
	## A chr pos
	with open(beda) as ainfo:
		adc = {}
		for i in ainfo:
			i = i.strip().split('\t')
			gene = i[3]
			CHR = i[0]
			if gene not in adc:
				adc[gene] = CHR
	### B chr pos
	with open(bedb) as binfo:
		bdc = {}
		for i in binfo:
			i = i.strip().split('\t')
			gene = i[3]
			CHR = i[0]
			if gene not in bdc:
				bdc[gene] = CHR
	###
	with open(blastfile) as blast:
		for i in blast:
			try:
				i = i.strip().split('\t')
				chra1 = adc[i[0]]
				chrb1 = bdc[i[1]]
				chra = re.sub('[0-9][0-9]|[0-9]','N',chra1)
				chrb = re.sub('[0-9][0-9]|[0-9]','N',chrb1)
				if re.search(matchA,chra) and re.search(matchB,chrb):
					#if re.search(matchA,chra).group()[A_num_index] == re.search(matchB,chrb).group()[B_num_index]:
					print ('\t'.join(i))
				elif re.search(matchA,chra) and ( not re.search(totalchrlist[1],chrb) ):
					print ('\t'.join(i))
				elif ( not re.search(totalchrlist[0],chra) ) and re.search(matchB,chrb):
					print ('\t'.join(i))
				elif ( not re.search(totalchrlist[0],chra)) and ( not re.search(totalchrlist[1],chrb) ):
					print ('\t'.join(i))
			except KeyError:
				continue
###
from optparse import OptionParser
def main():
	usage = "Usage: %prog -i blast_A_to_B -l A.bed -f B.bed -m chrNA,TuN\n" \
                "Author: Chen,Yongming; chen_ym@cau.edu.cn; 2019-12-14\n" \
                "Description: Match hit by same chromosome\n"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="blastfile",
                  help="blast_A_to_B", metavar="FILE")
	parser.add_option("-l", dest="beda",
                  help="A.bed", metavar="FILE")
	parser.add_option("-f", dest="bedb",
                  help="B.bed", metavar="FILE")
	parser.add_option("-m", dest="matchpair",
                  help="chrNA,TuN", metavar="FILE")
	parser.add_option("-t", dest="totalchr",
                  help="total chromosome file of re", metavar="FILE")
	(options, args) = parser.parse_args()
	Filter(options.blastfile,options.beda,options.bedb,options.matchpair,options.totalchr)
###
if __name__ == "__main__":
	main()
