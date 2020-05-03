#!/usr/bin/env python3
import sys
from math import log
#
data = open(sys.argv[1])
BBH = open(sys.argv[2])
BBHdc = {}
for i in BBH:
	i = i.strip().split('\t')
	if i[0] not in BBHdc:
		BBHdc[i[0]] = ''
	if i[1] not in BBHdc:
		BBHdc[i[1]] = ''
dc = {}
for i in data:
	i = i.strip().split('\t')
	value = float(i[2])
	if i[0] not in BBHdc:
		if not i[0] in dc:
			dc[i[0]] = {value:i[1]}
 		else:
			dc[i[0]][value] = i[1]
##
for i,j in dc.items():
	MAX = max(j.keys())
	gene = j[MAX]
	print str(i)+'\t'+str(gene)
