from __future__ import division 
import sys, argparse, os
import fileinput
import re
import statistics

# input arguments
parser = argparse.ArgumentParser(description="this script is to get mapping quality, allele frequency and alternative depth")

parser.add_argument('-vcf', '--normed_vcf', type=str, help='The VCF file you want to used',  required=True)
parser.add_argument('-prefix', '--prefix', type=str, help='Prefix of output file name',  required=True)

args = parser.parse_args()
normed_vcf = args.normed_vcf
prefix = args.prefix


file_name = prefix + '_variant_quality_location.vcf'
outfile = open(file_name,'w')

for line in fileinput.input(normed_vcf):
	m = re.match('^\#',line)
	if m is not None:
		outfile.write(line)
	else:
		line = line.strip()
		strings = line.split('\t')
		strings[8] = strings[8] + ':MQ:ALT:AF'
		infos = strings[7].strip().split(';')
		## MQ
		for element in infos:
			m = re.match('MQ=',element)
			if m is not None:
				MQ = element.split('=')[1]
		## ALT
		ad = strings[9].split(':')[1]
		ad_single = ad.split(',')
		ad_single = [int(i) for i in ad_single]
		DP = sum(ad_single)
		if DP != 0:
			ad_single.pop(0)
			ALT = sum(ad_single)
			AF = ALT/DP
		else:
			ALT = 0
			AF = 'NA'
		outLine = '\t'.join(strings) + ':' + MQ + ':' + str(ALT) + ':' + str(AF) + '\n'
		outfile.write(outLine)


		
		
