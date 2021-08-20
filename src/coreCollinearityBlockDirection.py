#!/usr/bin/env python3

'''
    genetribe - coreCBS.py
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
import pandas as pd
import numpy as np

def bed2dc(bedfile):
    bed2dc = {}
    with open(bedfile) as FILE:
        for i in FILE:
            i = i.strip().split('\t')
            bed2dc[i[3]] = int(i[1])
    return (bed2dc)

def get_direction(bed1,bed2,blockfile,outname):
    block_pos = open(outname+'.block_pos','w')
    with open(blockfile) as FILE:
        for i in FILE:
            if not i.startswith('#'):
                dc = {}
                i = i.strip().split('\t')
                pos_info = i[1].split(',')
                chr1 = pos_info[0].split(':')[0]
                start1 = pos_info[0].split(':')[1].split('-')[0]
                end1 = pos_info[0].split(':')[1].split('-')[1]
                chr2 = pos_info[1].split(':')[0]
                start2 = pos_info[1].split(':')[1].split('-')[0]
                end2 = pos_info[1].split(':')[1].split('-')[1]
                #
                info = i[5].split('; ')
                for j in range(len(info)):
                    if int(bed1[info[j].split(',')[0]]) not in dc:
                        dc[int(bed1[info[j].split(',')[0]])] = [int(bed2[info[j].split(',')[1]])]
                    else:
                        dc[int(bed1[info[j].split(',')[0]])].append(int(bed2[info[j].split(',')[1]]))
                for nnn in dc.keys():
                    dc[nnn] = np.median(dc[nnn])
                #
                pos1 = dc.keys()
                pos1 = sorted(pos1,reverse=True)
                total_stat = 0
                total = 0
                #
                if len(pos1) <= 10:
                    step = 1
                elif len(pos1) <= 40:
                    step = 2
                else:
                    step = len(pos1)//20
                #
                for k in range(len(pos1)):
                    total = total+1
                    if k == 0:
                        init = dc[pos1[k]]
                    if dc[pos1[k]] > init:
                        total_stat = total_stat+1
                    if total % step == 0:
                        init = dc[pos1[k]]
                if (total_stat/float(total)) < 0.5:
                    reverse = 'positive'
                else:
                    reverse = 'reverse'
                #print '\t'.join([chr1,start1,end1,chr2,start2,end2,i[4],reverse,str(total_stat/float(total))])
                block_pos.write('\t'.join([chr1,start1,end1,chr2,start2,end2,i[4],reverse])+'\n')

from optparse import OptionParser
def main():
    usage = "Usage: %prog -i collinearityInfo -a bed1 -b bed2 -o outname\n" \
            "Description: get direction of collinearity block"
    parser = OptionParser(usage)
    parser.add_option("-i", dest="blockfile",
                help="Collinearity info", metavar="FILE")
    parser.add_option("-a", dest="bed1",
                help="bed 1", metavar="FILE")
    parser.add_option("-b", dest="bed2",
                help="bed 2", metavar="FILE")
    parser.add_option("-o", dest="outname",
                help="prefix name of output file", metavar="STR")
    (options, args) = parser.parse_args()
    bed1tmp = bed2dc(options.bed1)
    bed2tmp = bed2dc(options.bed2)
    get_direction(bed1tmp,bed2tmp,options.blockfile,options.outname)

#
if __name__ == "__main__":
    main()