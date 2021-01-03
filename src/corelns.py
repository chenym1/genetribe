#!/usr/bin/env python3

'''
    genetribe - corelns.py
    Copyright (C) Yongming Chen
    Contact: chen_yongming@126.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
'''

import os
import subprocess
import sys

def sh(cmd_String):
	return subprocess.getstatusoutput(cmd_String)

#def changechrname(IN,OUT):
#	IN = open(IN).readlines()
#	OUT = open(OUT,'w')
#	for i in IN:
#		i = i.strip().split('\t')
#		i[0] = 'chr'+i[0]
#		OUT.write('\t'.join(i)+'\n')

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
		#
		#changechrname(bed_path1,out_dic+name1+'.bed')
		#changechrname(bed_path2,out_dic+name2+'.bed')
		sh(' '.join(['ln -s',bed_path1,out_dic+name1+'.bed']))
		sh(' '.join(['ln -s',bed_path2,out_dic+name2+'.bed']))
		sh(' '.join(['cat',name1+'.chrlist | gawk "{print $1}"','>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cat',name2+'.chrlist | gawk "{print $1}"','>>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cat',name2+'.chrlist | gawk "{print $1}"','>',out_dic+name2+'_'+name1+'.matchlist']))
		sh(' '.join(['cat',name1+'.chrlist | gawk "{print $1}"','>>',out_dic+name2+'_'+name1+'.matchlist']))
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
		sh(' '.join(['cat',name1+'.chrlist | gawk "{print $1}"','>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cat',name1+'.chrlist | gawk "{print $1}"','>>',out_dic+name1+'_'+name2+'.matchlist']))
		sh(' '.join(['cp',out_dic+name1+'_'+name2+'.matchlist',out_dic+name2+'_'+name1+'.matchlist']))
		if confidence_stat:
			confidence_path1 = os.path.abspath(name1+'.confidence')
			sh(' '.join(['ln -s',confidence_path1,out_dic+name1+'.confidence']))
			sh(' '.join(['ln -s',confidence_path1,out_dic+name2+'.confidence']))

from optparse import OptionParser
def main():
	usage = "Usage: %prog [options]\n" \
		"Description: prepare files"
	parser = OptionParser(usage)
	parser.add_option("-a", dest="name1",
		help="first name", metavar="STRING")
	parser.add_option("-b", dest="name2",
		help="second name", metavar="STRING")
	parser.add_option("-c", dest="confidence_stat",action="store_true",
		help="detect confidence file [Default: %default]",default=False)
	(options, args) = parser.parse_args()
	lns(options.name1,options.name2,options.confidence_stat)
#================
if __name__ == "__main__":
	main()
