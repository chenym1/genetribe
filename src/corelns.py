#!/usr/bin/env python3
import os
import subprocess
import sys
def sh(cmd_String):
	return subprocess.getstatusoutput(cmd_String)

def lns(name1,name2,confidence_stat):
	DIR=os.path.dirname(sys.argv[0])
	dirc = './output/'
	if name1 != name2:
		out_dic = './output/'
		sh(' '.join([DIR+'/coreFilterRedundancy','-i',dirc+name1+'_'+name2+'.blast','>',out_dic+name1+'_'+name2+'.blast2']))
		sh(' '.join([DIR+'/coreFilterRedundancy','-i',dirc+name1+'_'+name1+'.blast','>',out_dic+name1+'_'+name1+'.blast2']))
		sh(' '.join([DIR+'/coreFilterRedundancy','-i',dirc+name2+'_'+name1+'.blast','>',out_dic+name2+'_'+name1+'.blast2']))
		sh(' '.join([DIR+'/coreFilterRedundancy','-i',dirc+name2+'_'+name2+'.blast','>',out_dic+name2+'_'+name2+'.blast2']))
		blast_path1 = os.path.abspath(out_dic+name1+'_'+name2+'.blast2')
		blast_path2 = os.path.abspath(out_dic+name2+'_'+name1+'.blast2')
		sh(' '.join(['ln -s',blast_path1,out_dic+name1+'.'+name2+'.last']))
		sh(' '.join(['ln -s',blast_path2,out_dic+name2+'.'+name1+'.last']))
		bed_path1 = os.path.abspath(name1+'.bed')
		bed_path2 = os.path.abspath(name2+'.bed')
		sh(' '.join(['ln -s',bed_path1,out_dic+name1+'.bed']))
		sh(' '.join(['ln -s',bed_path2,out_dic+name2+'.bed']))
		sh(' '.join(['cat',name1+'.chrlist','>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cat',name2+'.chrlist','>>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cat',name2+'.chrlist','>',out_dic+name2+'_'+name1+'.matchlist']))
		sh(' '.join(['cat',name1+'.chrlist','>>',out_dic+name2+'_'+name1+'.matchlist']))
		if confidence_stat:
			confidence_path1 = os.path.abspath(name1+'.confidence')
			sh(' '.join(['ln -s',confidence_path1,out_dic+name1+'.confidence']))
			sh(' '.join(['ln -s',confidence_path1,out_dic+name2+'.confidence']))
	else:
		out_dic = './output/'
		name2 = name2+'itself'
		sh(' '.join([DIR+'/coreFilterRedundancy','-i',dirc+name1+'_'+name1+'.blast','>',out_dic+name1+'_'+name2+'.blast2']))
		blast_path1 = os.path.abspath(out_dic+name1+'_'+name2+'.blast2')
		sh(' '.join(['ln -s ',blast_path1,out_dic+name1+'_'+name1+'.blast2']))
		sh(' '.join(['ln -s ',blast_path1,out_dic+name2+'_'+name1+'.blast2']))
		sh(' '.join(['ln -s ',blast_path1,out_dic+name2+'_'+name2+'.blast2']))
		sh(' '.join(['ln -s ',blast_path1,out_dic+name1+'.'+name2+'.last']))
		sh(' '.join(['ln -s ',blast_path1,out_dic+name2+'.'+name1+'.last']))
		bed_path1 = os.path.abspath(name1+'.bed')
		sh(' '.join(['ln -s',bed_path1,out_dic+name1+'.bed']))
		sh(' '.join(['ln -s',bed_path1,out_dic+name2+'.bed']))
		sh(' '.join(['cat',name1+'.chrlist','>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cat',name1+'.chrlist','>>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cp',out_dic+name1+'_'+name2+'.matchlist',out_dic+name2+'_'+name1+'.matchlist']))
		if confidence_stat:
			confidence_path1 = os.path.abspath(name1+'.confidence')
			sh(' '.join(['ln -s',confidence_path1,out_dic+name1+'.confidence']))
			sh(' '.join(['ln -s',confidence_path1,out_dic+name2+'.confidence']))

from optparse import OptionParser
def main():
	usage = "Usage: %prog [options]\n" \
		"Description: link file.\n"\
		"Contact:     Chen, Yongming; chen_yongming@126.com;\n"\
		"Last Update: 2020-05-02"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="name1",
		help="First name", metavar="STRING")
	parser.add_option("-b", dest="name2",
		help="Second name", metavar="STRING")
	parser.add_option("-c", dest="confidence_stat",action="store_true",
		help="Confidence file detect [Default: %default]",default=False)
	(options, args) = parser.parse_args()
	lns(options.name1,options.name2,options.confidence_stat)
#================
if __name__ == "__main__":
	main()
