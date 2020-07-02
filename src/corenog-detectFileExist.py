#!/usr/bin/env python3

'''
    genetribe - corenog-detectFileExist.py
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


import sys
import datetime
import os
import concurrent.futures
import subprocess
import shutil

def sh(cmd_String):
	return subprocess.getstatusoutput(cmd_String)

def dicr_gg(dic):
	if not dic.endswith('/'):
		return dic+'/'
	else:
		return dic
	#
#
def detect_bed_file(name1,name2,confidence_stat=False):
	dicr = './'
	bed1 = dicr+name1+'.bed'
	bed2 = dicr+name2+'.bed'
	confidence1 = dicr+name1+'.confidence'
	confidence2 = dicr+name2+'.confidence'
	if confidence_stat:
		file_list = [bed1,bed2,confidence1,confidence2]
	else:
		file_list = [bed1,bed2]
	#
	not_exist_list = []
	for num in range(len(file_list)):
		if not os.path.exists(file_list[num]):
			not_exist_list.append(file_list[num])
		#
	#
	if len(not_exist_list) > 0 :
		print ("\n[ERROR]:\n\tFile cannot be found:"+' '.join(not_exist_list))
		exit(-1)
	#
#
def detect_blast_file(dicr,name1,name2):
	dicr = dicr_gg(dicr)
	if name1 != name2:
		blast_file1 = dicr+name1+'_'+name2+'.blast'
		blast_file2 = dicr+name2+'_'+name1+'.blast'
		onw_blast_file1 = dicr+name1+'_'+name1+'.blast'
		onw_blast_file2 = dicr+name2+'_'+name2+'.blast'
		file_list = [blast_file1,blast_file2,onw_blast_file1,onw_blast_file2]
		not_exist_list = []
		for num in range(4):
			if not os.path.exists(file_list[num]):
				not_exist_list.append(file_list[num])
			#
		#
	else:
		not_exist_list = []
		blast_file = dicr+name1+'_'+name2+'.blast'
		file_list = [blast_file]
		for num in range(1):
			if not os.path.exists(file_list[num]):
				not_exist_list.append(file_list[num])
			#
		#
	#
	return not_exist_list
#
def detect_fasta_file(name1,name2):
	dicr = './'
	fa1 = dicr+name1+'.fa'
	fa2 = dicr+name2+'.fa'
	long_fa1 = dicr+name1+'_long.fa'
	long_fa2 = dicr+name2+'_long.fa'
	file_list = [fa1,fa2]
	file_list2 = [long_fa1,long_fa2]
	not_exist_list = []
	for num in range(2):
		if not os.path.exists(file_list[num]):
			if not os.path.exists(file_list2[num]):
				not_exist_list.append(file_list[num])
			#
		#
	#
	return not_exist_list
#
def blast(dicr2,name1,name2,evalue,num_threads,fa_str="."):
	DIR = os.path.dirname(sys.argv[0])
	evalue=str(evalue)
	dicr2 = dicr_gg(dicr2)
	not_exist_blast = detect_blast_file(dicr2,name1,name2)
	dicr = './output/'
	tmp_out = './output/'
	if not os.path.exists(tmp_out):
		os.makedirs(tmp_out)
	else:
		shutil.rmtree(tmp_out)
	if len(not_exist_blast) == 0:
		if name1 != name2:
			sh('ln -s '+dicr2+name1+'_'+name2+'.blast '+dicr+name1+'_'+name2+'.blast')
			sh('ln -s '+dicr2+name2+'_'+name1+'.blast '+dicr+name2+'_'+name1+'.blast')
			sh('ln -s '+dicr2+name2+'_'+name2+'.blast '+dicr+name2+'_'+name2+'.blast')
			sh('ln -s '+dicr2+name1+'_'+name1+'.blast '+dicr+name1+'_'+name1+'.blast')
		else:
			sh('ln -s '+dicr2+name1+'_'+name1+'.blast '+dicr+name1+'_'+name1+'.blast')
	else:
		not_fasta = detect_fasta_file(name1,name2)
		if len(not_fasta) > 0:
			print ("\n[ERROR]:\n\t File cannot be found:"+' '.join(not_fasta))
			exit(-1)
		else:
			num_threads = int(num_threads)//len(not_exist_blast)
			if num_threads == 0:
				num_threads = 1
			if name1 != name2 :
				#
				fa1 = './'+name1+'.fa'
				fa2 = './'+name2+'.fa'
				raw_long_fa1 = './'+name1+'_long.fa'
				raw_long_fa2 = './'+name2+'_long.fa'
				long_fa1 = tmp_out+name1+'_long.fa'
				long_fa2 = tmp_out+name2+'_long.fa'
				db1 = tmp_out+name1+'_db/'+name1
				db2 = tmp_out+name2+'_db/'+name2
				#
				if not os.path.exists(raw_long_fa1):
					sh(DIR+'/longestfasta -i '+fa1+' -s '+fa_str+' > '+long_fa1)
				else:
					sh('cp '+raw_long_fa1+' '+long_fa1)

				if not os.path.exists(raw_long_fa2):
					sh(DIR+'/longestfasta -i '+fa2+' -s '+fa_str+' > '+long_fa2)
				else:
					sh('cp '+raw_long_fa2+' '+long_fa2)
				#
				sh('makeblastdb -in '+long_fa1+' -parse_seqids -hash_index -dbtype prot -out '+db1)
				sh('makeblastdb -in '+long_fa2+' -parse_seqids -hash_index -dbtype prot -out '+db2)
				#
				blast_task = []
				if dicr2+name1+'_'+name2+'.blast' in not_exist_blast:
					blast_task.append('blastp -query '+long_fa1+' -db '+db2+' -evalue '+evalue+' -num_threads '+str(num_threads)+' -outfmt 6 -out '+dicr+name1+'_'+name2+'.blast')
				else:
					sh('ln -s '+dicr2+name1+'_'+name2+'.blast '+dicr+name1+'_'+name2+'.blast')
				if dicr2+name2+'_'+name1+'.blast' in not_exist_blast:
					blast_task.append('blastp -query '+long_fa2+' -db '+db1+' -evalue '+evalue+' -num_threads '+str(num_threads)+' -outfmt 6 -out '+dicr+name2+'_'+name1+'.blast')
				else:
					sh('ln -s '+dicr2+name2+'_'+name1+'.blast '+dicr+name2+'_'+name1+'.blast')
				if dicr2+name1+'_'+name1+'.blast' in not_exist_blast:
					blast_task.append('blastp -query '+long_fa1+' -db '+db1+' -evalue '+evalue+' -num_threads '+str(num_threads)+' -outfmt 6 -out '+dicr+name1+'_'+name1+'.blast')
				else:
					sh('ln -s '+dicr2+name1+'_'+name1+'.blast '+dicr+name1+'_'+name1+'.blast')
				if dicr2+name2+'_'+name2+'.blast' in not_exist_blast:
					blast_task.append('blastp -query '+long_fa2+' -db '+db2+' -evalue '+evalue+' -num_threads '+str(num_threads)+' -outfmt 6 -out '+dicr+name2+'_'+name2+'.blast')
				else:
					sh('ln -s '+dicr2+name2+'_'+name2+'.blast '+dicr+name2+'_'+name2+'.blast')
				with concurrent.futures.ProcessPoolExecutor() as executor:
					executor.map(sh,blast_task)
				#
			else:
				fa1 = dicr+name1+'.fa'
				long_fa1 = tmp_out+name1+'_long.fa'
				db1 = tmp_out+name1+'_db/'+name1
				sh(DIR+'/longestfasta -i '+fa1+' -s '+fa_str+' > '+long_fa1)
				sh('makeblastdb -in '+long_fa1+' -parse_seqids -hash_index -dbtype prot -out '+db1)
				blast_task = ['blastp -query '+long_fa1+' -db '+db1+' -evalue '+evalue+' -num_threads '+str(num_threads)+' -outfmt 6 -out '+dicr+name1+'_'+name1+'.blast']
				sh(blast_task[0])
		#
	#
#
def detect_total(dicr,name1,name2,evalue = 1e-5,num_threads = 36,fa_str = ".",confidence_stat = False):
	detect_bed_file(name1,name2,confidence_stat)
	blast(dicr,name1,name2,evalue,num_threads,fa_str)

from optparse import OptionParser
def main():
	usage = "Usage: %prog [options] \n"\
		"Description: Check for file existence and blast (nog).\n"\
		"Contact:     Chen, Yongming; chen_yongming@126.com;\n"\
		"Last Update: 2020-07-02"
	parser = OptionParser(usage)
	parser.add_option("-d", dest="directory",
		help="Pre-computed BLAST file in <dir> [Default: %default]", metavar="DIRECTORY",default='./')
	parser.add_option("-a", dest="name1",
		help="First name", metavar="STRING")
	parser.add_option("-b", dest="name2",
		help="Second name", metavar="STRING")
	parser.add_option("-e", dest="evalue",metavar="",
		help="E-value for BLASTP [Default: %default]",default=1e-5)
	parser.add_option("-n", dest="num_threads",metavar="INT",
		help="Num threads for BLASTP [Default: %default]",default=36)
	parser.add_option("-f", dest="fa_str",metavar="STRING",
		help="The separator between gene name and number in the header of fasta [Default: %default]",default=".")
	parser.add_option("-c", dest="confidence_stat",action="store_true",
		help="Confidence file detect [Default: %default]",default=False)
	(options, args) = parser.parse_args()
	detect_total(options.directory,options.name1,options.name2,options.evalue,options.num_threads,options.fa_str,options.confidence_stat)
#===================================

if __name__ == "__main__":
	main()
