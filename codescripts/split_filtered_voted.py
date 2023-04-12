import pandas as pd
import os
import sys, argparse, os


# input arguments
parser = argparse.ArgumentParser(description="this script is to exclude indel over 50bp")

parser.add_argument('-a', '--sample_vcf', type=str, help='All variants from a specific sample',  required=True)
parser.add_argument('-f', '--filtered', type=str, help='Filtered variants',  required=True)
parser.add_argument('-v', '--voted', type=str, help='Voted variants by replicates',  required=True)
parser.add_argument('-p', '--prefix', type=str, help='Prefix of output file',  required=True)



args = parser.parse_args()
vcf = args.sample_vcf
filtered = args.filtered
voted = args.voted
prefix = args.prefix

vcf_dat = pd.read_table(vcf,header=None)
filtered_dat = pd.read_table(filtered,header=None)
voted_dat = pd.read_table(voted,header=None)
merged_filtered_df = pd.merge(vcf_dat, filtered_dat,  how='inner', left_on=[0,1], right_on = [0,1])
merged_voted_df = pd.merge(vcf_dat, voted_dat,  how='inner', left_on=[0,1], right_on = [0,1])

filtered_name = prefix + '.filtered.bed'
filtered_file = open(filtered_name,'w')

voted_name = prefix + '.voted.bed'
voted_file = open(voted_name,'w')


for row in merged_filtered_df.itertuples():
	if ',' in row._4:
		alt_strings = row._4.split(',')
		alt_len = [len(i) for i in alt_strings]
		alt = max(alt_len)
	else:
		alt = len(row._4)
	ref = row._3
	pos = row._2
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
	outline = row._1 + '\t' + str(StartPos) + '\t' + str(EndPos) + '\t' + cate + '\t' + row._5 +'\n'
	filtered_file.write(outline)

for row in merged_voted_df.itertuples():
	if ',' in row._4:
		alt_strings = row._4.split(',')
		alt_len = [len(i) for i in alt_strings]
		alt = max(alt_len)
	else:
		alt = len(row._4)
	ref = row._3
	pos = row._2
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
	outline = row._1 + '\t' + str(StartPos) + '\t' + str(EndPos) + '\t' + cate + '\t' + row._5 +'\n'
	voted_file.write(outline)







