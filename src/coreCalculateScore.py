#!/usr/bin/env python3
import re

# print chromosome information
def printchr ( chrlist ):
	list1 = []
	for i in range(len(chrlist)):
		info = re.sub('N','[0-9]',chrlist[i])
		info2 = re.sub('N','[0-9][0-9]',chrlist[i])
		list1.append(info)
		list1.append(info2)
	return '|'.join(list1)

# Convert confidence's files to dict
def confidence2dc (confidencd_file):
	typedc = {}
	with open(confidencd_file) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			typedc[i[0]] = i[1]
	return typedc

# Convert bed files to dict
def bed2dc (bed_file):
	beddc = {}
	with open(bed_file) as FILE:
		for i in FILE:
			i = i.strip().split('\t')
			beddc[i[3]] = i[0]
	return beddc

# Convert bitscore file to dict:
def bitscore2dc (own_file):
	dc = {}
	with open(own_file) as own:
		for i in own:
			i = i.strip().split('\t')
			dc[i[0]] = i[11]
	return dc
#
def Filter ( blastfile,matchpair,beda,bedb,owna,ownb,typea,typeb,stat_chromosome,stat_confidence,out_chr_info ) :
	## type dict
	if stat_confidence:
		typeadc = confidence2dc(typea)
		typebdc = confidence2dc(typeb)
	## bed dict
	if stat_chromosome:
		beddca = bed2dc(beda)
		beddcb = bed2dc(bedb)
	## bitscore into dict
	adc = bitscore2dc(owna)
	bdc = bitscore2dc(ownb)
	### total chr
	with open(matchpair) as FILE:
		match_list = []
		CHR_1 = []
		CHR_2 = []
		info1 = FILE.readline().strip().split(',')
		for i in range(len(info1)):
			CHR = info1[i]
			CHR_1.append(CHR)
		info2 = FILE.readline().strip().split(',')
		for i in range(len(info2)):
			CHR = info2[i]
			CHR_2.append(CHR)
		chrlist1 = '|'.join(CHR_1)
		chrlist2 = '|'.join(CHR_2)
		prefix_chr = [CHR_1,CHR_2]
		#print prefix_chr
	#
	chrinfo1 = printchr(CHR_1)
	chrinfo2 = printchr(CHR_2)
	#
	out = open(out_chr_info,'w')
	out.write(chrlist1+'\t'+chrlist2)
	out.close()
	## get score
	'''
	filter similarity of pairs
	'''
	with open(blastfile) as blast:
		for i in blast:
			i = i.strip().split('\t')
			geneA = i[0]
			geneB = i[1]
			if geneA != geneB:
				#=======   BSR   ================
				bitscore = i[11]
				try:
					bitAB = float(bdc[geneB])
					bitOb = float(bitscore)/float(bitAB)
				except KeyError:
					try:
						bitAB = float(adc[geneA])
						bitOb = float(bitscore)/float(bitAB)
					except KeyError:
						continue
				#======  chromosome group  ======
				if stat_chromosome:
					try:
						chra = beddca[geneA]
						chrb = beddcb[geneB]
					except KeyError:
						continue
					chromosome_group = 2
					if re.search(chrinfo1,chra) and re.search(chrinfo2,chrb):
						chr_in_1 = re.search(chrinfo1,chra).group()
						chr_in_2 = re.search(chrinfo2,chrb).group()
						chr_groupA = re.findall(r'\d+',chr_in_1)[0]
						chr_groupB = re.findall(r'\d+',chr_in_2)[0]
						if chr_groupA == chr_groupB:
							chromosome_group = 0
				else:
					chromosome_group = 0
				#======  confidance  =======
				if stat_confidence:
					try:
						type_1 = typeadc[geneA]
						type_2 = typebdc[geneB]
					except KeyError:
                       	                	continue
					if type_1 == "HC" and type_2 == "HC":
						confidence = 0
					elif type_1 == "LC" and type_2 == "LC":
						confidence = 2
					else:
						confidence = 1
				else:
					confidence = 0
				##
				bitOb = '%.3f' % bitOb
				gene_score = chromosome_group+confidence
				print (geneA+'\t'+geneB+'\t'+str(bitOb)+'\t'+str(gene_score))

####
from optparse import OptionParser
def main():
	usage = "Usage: %prog -i \n" \
		"Author: Chen,Yongming; chen_ym@cau.edu.cn; 2019-12-13\n" \
		"Description: Get BSR and chromosome-group score of every hits"
	parser = OptionParser(usage)
	parser.add_option("-i", dest="blastfile",
                  help="A blast B file", metavar="FILE")
	parser.add_option("-m", dest="matchpair",
                  help="homoeolog chromosome group", metavar="FILE")
	parser.add_option("-a", dest="beda",
                  help="bed of A genome", metavar="FILE")
	parser.add_option("-b", dest="bedb",
                  help="bed of B genome", metavar="FILE")
	parser.add_option("--oa", dest="owna",
                  help="self-blast of A genome", metavar="FILE")
	parser.add_option("--ob", dest="ownb",
                  help="self-blast of B genome", metavar="FILE")
	parser.add_option("--ta", dest="typea",
                  help="confidence type of A genome", metavar="FILE")
	parser.add_option("--tb", dest="typeb",
                  help="confidence type of B genome", metavar="FILE")
	parser.add_option("-r", action="store_false",  dest = "stat_chromosome",
		help="Whether to count chromosome score [default: %default]",default = True, metavar="boolean")
	parser.add_option("-c", action="store_true",  dest = "stat_confidence",
	        help="Whether to count confidence score [default: %default]",default = False, metavar="boolean")
	parser.add_option("-o", dest="out_chr_info",
                  help="out chromosome information chrNA|chrNB TuN", metavar="FILE")
	(options, args) = parser.parse_args()
	Filter(options.blastfile,options.matchpair,options.beda,options.bedb,options.owna,options.ownb,options.typea,options.typeb,options.stat_chromosome,options.stat_confidence,options.out_chr_info)
###
if __name__ == "__main__":
	main()
