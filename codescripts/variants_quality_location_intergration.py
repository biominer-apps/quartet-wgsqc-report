import sys, argparse, os
import fileinput
import re
import statistics

# input arguments
parser = argparse.ArgumentParser(description="this script is to intergeate vcf information, variants quality and location")

parser.add_argument('-vcf', '--multi_sample_vcf', type=str, help='The VCF file you want to count the voting number',  required=True)
parser.add_argument('-prefix', '--prefix', type=str, help='Prefix of output file name',  required=True)

args = parser.parse_args()
multi_sample_vcf = args.multi_sample_vcf
prefix = args.prefix


def get_location(info):
	repeat = ''
	if 'ANN' in info:
		strings = info.strip().split(';')
		for element in strings:
			m = re.match('ANN',element)
			if m is not None:
				repeat = element.split('=')[1]
	else:
		repeat = '.'
	return repeat


def extract_info_normal(FORMAT,strings):
	GQ = []
	MQ = []
	DP = []
	ALT = []
	format_strings = FORMAT.split(':')
	for element in strings:
		if element == '.':
			pass
		else:
			element_strings = element.split(':')
			formatDict = dict(zip(format_strings, element_strings))		
			alt = int(formatDict['ALT'])
			dp = int(formatDict['DP'])
			gq = int(formatDict['GQ'])
			mq = float(formatDict['MQ'])
			GQ.append(gq)
			MQ.append(mq)
			DP.append(dp)
			ALT.append(alt)
	DP_a = sum(DP)
	ALT_a = sum(ALT)
	if DP_a == 0:
		AF_m = 'NA'
	else:
		AF_m = float(ALT_a/DP_a)
	GQ_m = statistics.mean(GQ)
	MQ_m = statistics.mean(MQ)
	return AF_m,GQ_m,MQ_m,DP_a,ALT_a


file_name = prefix + '_variant_quality_location.txt'
outfile = open(file_name,'w')
outputcolumn = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tQuartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5\tQuartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5\tQuartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5\tQuartet_DNA_BGI_T7_WGE_1_20191105_LCL5\tQuartet_DNA_BGI_T7_WGE_2_20191105_LCL5\tQuartet_DNA_BGI_T7_WGE_3_20191105_LCL5\tQuartet_DNA_ILM_Nova_ARD_1_20181108_LCL5\tQuartet_DNA_ILM_Nova_ARD_2_20181108_LCL5\tQuartet_DNA_ILM_Nova_ARD_3_20181108_LCL5\tQuartet_DNA_ILM_Nova_ARD_4_20190111_LCL5\tQuartet_DNA_ILM_Nova_ARD_5_20190111_LCL5\tQuartet_DNA_ILM_Nova_ARD_6_20190111_LCL5\tQuartet_DNA_ILM_Nova_BRG_1_20180930_LCL5\tQuartet_DNA_ILM_Nova_BRG_2_20180930_LCL5\tQuartet_DNA_ILM_Nova_BRG_3_20180930_LCL5\tQuartet_DNA_ILM_Nova_WUX_1_20190917_LCL5\tQuartet_DNA_ILM_Nova_WUX_2_20190917_LCL5\tQuartet_DNA_ILM_Nova_WUX_3_20190917_LCL5\tQuartet_DNA_ILM_XTen_ARD_1_20170403_LCL5\tQuartet_DNA_ILM_XTen_ARD_2_20170403_LCL5\tQuartet_DNA_ILM_XTen_ARD_3_20170403_LCL5\tQuartet_DNA_ILM_XTen_NVG_1_20170329_LCL5\tQuartet_DNA_ILM_XTen_NVG_2_20170329_LCL5\tQuartet_DNA_ILM_XTen_NVG_3_20170329_LCL5\tQuartet_DNA_ILM_XTen_WUX_1_20170216_LCL5\tQuartet_DNA_ILM_XTen_WUX_2_20170216_LCL5\tQuartet_DNA_ILM_XTen_WUX_3_20170216_LCL5' +'\t'+ 'location' + '\t' + 'AF' + '\t' + 'GQ' + '\t' + 'MQ' + '\t' + 'DP' + '\t' + 'ALT' +'\n'
outfile.write(outputcolumn)

for line in fileinput.input(multi_sample_vcf):
	m = re.match('^\#',line)
	if m is not None:
		pass
	else:
		line = line.strip()
		strings = line.split('\t')
		repeat = get_location(strings[7])
		AF,GQ,MQ,DP,ALT = extract_info_normal(strings[8],strings[9:])
		outLine = '\t'.join(strings) + '\t' + repeat +'\t' + str(AF) + '\t' + str(GQ) + '\t' + str(MQ) + '\t' + str(DP) + '\t' + str(ALT) + '\n'
		outfile.write(outLine)


		
		
