import sys,getopt
import os
import fileinput
outFile = open(sys.argv[2],'w')
for line in fileinput.input(sys.argv[1]):
	line = line.rstrip()
	strings = line.strip().split('\t')
#d5
	if ',' in strings[6]:
		alt_strings = strings[6].split(',')
		alt_len = [len(i) for i in alt_strings]
		alt = max(alt_len)
	else:
		alt = len(strings[6])
	ref = strings[5]
	pos = int(strings[1])
	if len(ref) == 1 and alt == 1:
		StartPos = int(pos) -1
		EndPos = int(pos)
		cate = 'SNV'
	elif len(ref) > alt:
		StartPos = int(pos) - 1
		EndPos = int(pos) + (len(ref) - 1)
		cate = 'INDEL'
	elif alt > len(ref):
		StartPos = int(pos) - 1
		EndPos = int(pos) + (alt - 1)
		cate = 'INDEL'
	elif len(ref) == alt:
		StartPos = int(pos) - 1
		EndPos = int(pos) + (alt - 1)
		cate = 'INDEL'
	outline = '\t'.join(strings) + '\t' + str(StartPos) + '\t' + str(EndPos) + '\t' + cate + '\n'
	outFile.write(outline)








