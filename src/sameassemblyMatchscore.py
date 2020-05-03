#!/usr/bin/env python3
import sys
#
Adc = {}
with open(sys.argv[1]) as f:
	for i in f:
		i = i.strip().split('\t')
		Adc[i[0]] = i[1]
#
with open(sys.argv[2]) as f:
	for i in f:
		i = i.strip().split('\t')
		length = float(Adc[i[0]])
		overlap = float(i[2])
		score = (overlap/length)*100
		score = '%.2f' % score
		print i[0]+'\t'+i[1]+'\t'+str(score)
