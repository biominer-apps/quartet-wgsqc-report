import pandas as pd
import sys, argparse, os
import fileinput
import re

# input arguments
parser = argparse.ArgumentParser(description="this script is to get final high confidence calls and information of all replicates")

parser.add_argument('-vcfInfo', '--vcfInfo', type=str, help='The txt file of variants information, this file is named as prefix__variant_quality_location.txt',  required=True)
parser.add_argument('-mendelianInfo', '--mendelianInfo', type=str, help='The merged mendelian information of all samples',  required=True)
parser.add_argument('-prefix', '--prefix', type=str, help='The prefix of output filenames',  required=True)
parser.add_argument('-sample', '--sample_name', type=str, help='which sample of quartet',  required=True)


args = parser.parse_args()
vcfInfo = args.vcfInfo
mendelianInfo = args.mendelianInfo
prefix = args.prefix
sample_name = args.sample_name

vcf_header = '''##fileformat=VCFv4.2
##fileDate=20200331
##source=high_confidence_calls_intergration(choppy app)
##reference=GRCh38.d1.vd1
##INFO=<ID=location,Number=1,Type=String,Description="Repeat region">
##INFO=<ID=DPCT,Number=1,Type=Float,Description="Percentage of detected votes">
##INFO=<ID=VPCT,Number=1,Type=Float,Description="Percentage of consnesus votes">
##INFO=<ID=FPCT,Number=1,Type=Float,Description="Percentage of mendelian consisitent votes">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Int,Description="Depth">
##FORMAT=<ID=AF,Number=1,Type=Float,Description="Allele frequency">
##FORMAT=<ID=GQ,Number=1,Type=Float,Description="Genotype quality">
##FORMAT=<ID=MQ,Number=1,Type=Float,Description="Mapping quality">
##contig=<ID=chr1,length=248956422>
##contig=<ID=chr2,length=242193529>
##contig=<ID=chr3,length=198295559>
##contig=<ID=chr4,length=190214555>
##contig=<ID=chr5,length=181538259>
##contig=<ID=chr6,length=170805979>
##contig=<ID=chr7,length=159345973>
##contig=<ID=chr8,length=145138636>
##contig=<ID=chr9,length=138394717>
##contig=<ID=chr10,length=133797422>
##contig=<ID=chr11,length=135086622>
##contig=<ID=chr12,length=133275309>
##contig=<ID=chr13,length=114364328>
##contig=<ID=chr14,length=107043718>
##contig=<ID=chr15,length=101991189>
##contig=<ID=chr16,length=90338345>
##contig=<ID=chr17,length=83257441>
##contig=<ID=chr18,length=80373285>
##contig=<ID=chr19,length=58617616>
##contig=<ID=chr20,length=64444167>
##contig=<ID=chr21,length=46709983>
##contig=<ID=chr22,length=50818468>
##contig=<ID=chrX,length=156040895>
'''

vcf_header_all_sample = '''##fileformat=VCFv4.2
##fileDate=20200331
##reference=GRCh38.d1.vd1
##INFO=<ID=location,Number=1,Type=String,Description="Repeat region">
##INFO=<ID=DPCT,Number=1,Type=Float,Description="Percentage of detected votes">
##INFO=<ID=VPCT,Number=1,Type=Float,Description="Percentage of consnesus votes">
##INFO=<ID=FPCT,Number=1,Type=Float,Description="Percentage of mendelian consisitent votes">
##INFO=<ID=ALL_ALT,Number=1,Type=Float,Description="Sum of alternative reads of all samples">
##INFO=<ID=ALL_DP,Number=1,Type=Float,Description="Sum of depth of all samples">
##INFO=<ID=ALL_AF,Number=1,Type=Float,Description="Allele frequency of net alternatice reads and net depth">
##INFO=<ID=GQ_MEAN,Number=1,Type=Float,Description="Mean of genotype quality of all samples">
##INFO=<ID=MQ_MEAN,Number=1,Type=Float,Description="Mean of mapping quality of all samples">
##INFO=<ID=PCR,Number=1,Type=String,Description="Consensus of PCR votes">
##INFO=<ID=PCR_FREE,Number=1,Type=String,Description="Consensus of PCR-free votes">
##INFO=<ID=CONSENSUS,Number=1,Type=String,Description="Consensus calls">
##INFO=<ID=CONSENSUS_SEQ,Number=1,Type=String,Description="Consensus sequence">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=String,Description="Depth">
##FORMAT=<ID=AF,Number=1,Type=String,Description="Allele frequency">
##FORMAT=<ID=GQ,Number=1,Type=String,Description="Genotype quality">
##FORMAT=<ID=MQ,Number=1,Type=String,Description="Mapping quality">
##FORMAT=<ID=TWINS,Number=1,Type=String,Description="1 is twins shared, 0 is twins discordant ">
##FORMAT=<ID=TRIO5,Number=1,Type=String,Description="1 is LCL7, LCL8 and LCL5 mendelian consistent, 0 is mendelian vioaltion">
##FORMAT=<ID=TRIO6,Number=1,Type=String,Description="1 is LCL7, LCL8 and LCL6 mendelian consistent, 0 is mendelian vioaltion">
##contig=<ID=chr1,length=248956422>
##contig=<ID=chr2,length=242193529>
##contig=<ID=chr3,length=198295559>
##contig=<ID=chr4,length=190214555>
##contig=<ID=chr5,length=181538259>
##contig=<ID=chr6,length=170805979>
##contig=<ID=chr7,length=159345973>
##contig=<ID=chr8,length=145138636>
##contig=<ID=chr9,length=138394717>
##contig=<ID=chr10,length=133797422>
##contig=<ID=chr11,length=135086622>
##contig=<ID=chr12,length=133275309>
##contig=<ID=chr13,length=114364328>
##contig=<ID=chr14,length=107043718>
##contig=<ID=chr15,length=101991189>
##contig=<ID=chr16,length=90338345>
##contig=<ID=chr17,length=83257441>
##contig=<ID=chr18,length=80373285>
##contig=<ID=chr19,length=58617616>
##contig=<ID=chr20,length=64444167>
##contig=<ID=chr21,length=46709983>
##contig=<ID=chr22,length=50818468>
##contig=<ID=chrX,length=156040895>
'''

# output file
file_name = prefix + '_benchmarking_calls.vcf'
outfile = open(file_name,'w')

all_sample_file_name = prefix + '_all_sample_information.vcf'
all_sample_outfile = open(all_sample_file_name, 'w')

# write VCF
outputcolumn = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t' + sample_name + '_high_confidence_calls\n'
outfile.write(vcf_header)
outfile.write(outputcolumn)

outputcolumn_all_sample = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'+ \
'Quartet_DNA_BGI_SEQ2000_BGI_1_20180518\tQuartet_DNA_BGI_SEQ2000_BGI_2_20180530\tQuartet_DNA_BGI_SEQ2000_BGI_3_20180530\t' + \
'Quartet_DNA_BGI_T7_WGE_1_20191105\tQuartet_DNA_BGI_T7_WGE_2_20191105\tQuartet_DNA_BGI_T7_WGE_3_20191105\t' + \
'Quartet_DNA_ILM_Nova_ARD_1_20181108\tQuartet_DNA_ILM_Nova_ARD_2_20181108\tQuartet_DNA_ILM_Nova_ARD_3_20181108\t' + \
'Quartet_DNA_ILM_Nova_ARD_4_20190111\tQuartet_DNA_ILM_Nova_ARD_5_20190111\tQuartet_DNA_ILM_Nova_ARD_6_20190111\t' + \
'Quartet_DNA_ILM_Nova_BRG_1_20180930\tQuartet_DNA_ILM_Nova_BRG_2_20180930\tQuartet_DNA_ILM_Nova_BRG_3_20180930\t' + \
'Quartet_DNA_ILM_Nova_WUX_1_20190917\tQuartet_DNA_ILM_Nova_WUX_2_20190917\tQuartet_DNA_ILM_Nova_WUX_3_20190917\t' + \
'Quartet_DNA_ILM_XTen_ARD_1_20170403\tQuartet_DNA_ILM_XTen_ARD_2_20170403\tQuartet_DNA_ILM_XTen_ARD_3_20170403\t' + \
'Quartet_DNA_ILM_XTen_NVG_1_20170329\tQuartet_DNA_ILM_XTen_NVG_2_20170329\tQuartet_DNA_ILM_XTen_NVG_3_20170329\t' + \
'Quartet_DNA_ILM_XTen_WUX_1_20170216\tQuartet_DNA_ILM_XTen_WUX_2_20170216\tQuartet_DNA_ILM_XTen_WUX_3_20170216\n'
all_sample_outfile.write(vcf_header_all_sample)
all_sample_outfile.write(outputcolumn_all_sample)

# input files
vcf_info = pd.read_table(vcfInfo)
mendelian_info = pd.read_table(mendelianInfo)

merged_df = pd.merge(vcf_info, mendelian_info,  how='outer', left_on=['#CHROM','POS','REF'], right_on = ['#CHROM','POS','REF'])
merged_df = merged_df.fillna('.')

# function
def single_sample_format(format_x,strings_x,strings_y):
	gt = '.'
	dp = '.'
	af = '.'
	gq = '.'
	mq = '.'
	twins = '.'
	trio5 = '.'
	trio6 = '.'
	# GT:DP:AF:GQ:MQ:TWINS:TRIO5:TRIO6
	# strings_x
	format_strings = format_x.split(':')
	if (strings_x == '.') and (strings_y != '.'):
		element_strings_y = str(strings_y).split(':')
		gt = '0/0'
		dp = '.'
		af = '.'
		gq = '.'
		mq = '.'
		twins = element_strings_y[1]
		trio5 = element_strings_y[2]
		trio6 = element_strings_y[3]		
	elif (strings_x != '.') and (strings_y == '.'):
		element_strings_x = strings_x.split(':')
		formatDict = dict(zip(format_strings, element_strings_x))
		gt = formatDict['GT']
		dp = formatDict['DP']
		af = formatDict['AF']
		gq = formatDict['GQ']
		mq = formatDict['MQ']
		twins = '.'
		trio5 = '.'
		trio6 = '.'
	elif (strings_x != '.') and (strings_y != '.'):
		element_strings_y = str(strings_y).split(':')
		element_strings_x = strings_x.split(':')
		formatDict = dict(zip(format_strings, element_strings_x))
		gt = formatDict['GT']
		dp = formatDict['DP']
		af = formatDict['AF']
		gq = formatDict['GQ']
		mq = formatDict['MQ']
		twins = element_strings_y[1]
		trio5 = element_strings_y[2]
		trio6 = element_strings_y[3]				
	else:
		pass
	merged_format = gt + ':' + dp + ':' + af + ':' + gq + ':' + mq + ':' + twins + ':' + trio5 + ':' + trio6
	return(merged_format)

#
for row in merged_df.itertuples():
	info = 'location=' + str(row.location) + ';' + str(row.INFO_y)
	if row.FILTER_y == 'reproducible':
		ref = row.DP - row._42
		FORMAT = row[77] + ':' + str(int(ref)) + ',' + str(int(row._42)) + ':' + str(int(row.DP)) + ':' + str(round(row.AF,2)) + ':' + str(round(row.GQ,2)) + ':' + str(round(row.MQ,2))
		outline1 = str(row._1) + '\t' + str(row.POS) + '\t' + str(row.ID_x) + '\t' +  str(row.REF) + '\t' + str(row[78]) + '\t' + '.' + '\t' + '.' + '\t' + str(info) + '\t' + 'GT:AD:DP:AF:GQ:MQ' + '\t' + str(FORMAT) + '\n'
		outfile.write(outline1)
	else:
		pass
	if row.INFO_x != '.':
		info = 'location=' + str(row.location) + ';' + str(row.INFO_y) + ';' + 'ALL_ALT=' + str(int(row._42)) + ';' + 'ALL_DP=' + str(int(row.DP)) + ';' + 'ALL_AF=' + str(round(row.AF,1)) + ';' + 'GQ_MEAN=' + str(round(row.GQ,1)) + ';' + 'MQ_MEAN=' + str(round(row.MQ,1)) + ';' + 'PCR=' + str(row[75]) + ';' + 'PCR_FREE=' + str(row[76]) + ';' + 'CONSENSUS=' + str(row[77]) + ';' + 'CONSENSUS_SEQ=' + str(row[78])
		Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5_x, row.Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5_y)
		Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5_x, row.Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5_y)
		Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5_x, row.Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5_y)
		Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5_x, row.Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5_y)
		Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5_x, row.Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5_y)
		Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5_x, row.Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5_y)
		Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5_x, row.Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5_y)
		Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5_x, row.Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5_y)
		Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5_x, row.Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5_y)
		Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5_x, row.Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5_y)
		Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5_x, row.Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5_y)
		Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5_x, row.Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5_y)
		Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5_x, row.Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5_y)
		Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5_x, row.Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5_y)
		Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5_x, row.Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5_y)
		Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5_x, row.Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5_y)
		Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5_x, row.Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5_y)
		Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5_x, row.Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5_y)
		Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5_x, row.Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5_y)
		Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5_x, row.Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5_y)
		Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5_x, row.Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5_y)
		outline2 = str(row._1) + '\t' + str(row.POS) + '\t' + str(row.ID_x) +'\t' + str(row.REF) + '\t' + str(row[5]) + '\t' + '.' + '\t' + '.' + '\t' + str(info) + '\t' + 'GT:DP:AF:GQ:MQ:TWINS:TRIO5:TRIO6' + '\t' \
		+ str(Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5) + '\t' + str(Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5) + '\t' + str(Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5) + '\t' \
		+ str(Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5) + '\t' + str(Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5) + '\t' + str(Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5)  + '\t' + str(Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5) + '\n'
		all_sample_outfile.write(outline2)
	else:
		info = '.'
		Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5_x, row.Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5_y)
		Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5_x, row.Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5_y)
		Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5_x, row.Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5_y)
		Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5_x, row.Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5_y)
		Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5_x, row.Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5_y)
		Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5_x, row.Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5_y)
		Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5_x, row.Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5_y)
		Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5_x, row.Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5_y)
		Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5_x, row.Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5_y)
		Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5_x, row.Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5_y)
		Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5_x, row.Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5_y)
		Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5_x, row.Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5_y)
		Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5_x, row.Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5_y)
		Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5_x, row.Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5_y)
		Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5_x, row.Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5_y)
		Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5_x, row.Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5_y)
		Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5_x, row.Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5_y)
		Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5_x, row.Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5_y)
		Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5_x, row.Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5_y)
		Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5_x, row.Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5_y)
		Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5_x, row.Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5_y)
		Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5 = single_sample_format(row.FORMAT_x, row.Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5_x, row.Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5_y)
		outline2 = str(row._1) + '\t' + str(row.POS) + '\t' + str(row.ID_x) +'\t' + str(row.REF) + '\t' + str(row[5]) + '\t' + '.' + '\t' + '.' + '\t' + str(info) + '\t' + 'GT:DP:AF:GQ:MQ:TWINS:TRIO5:TRIO6' + '\t' \
		+ str(Quartet_DNA_BGI_SEQ2000_BGI_1_20180518_LCL5) + '\t' + str(Quartet_DNA_BGI_SEQ2000_BGI_2_20180530_LCL5) + '\t' + str(Quartet_DNA_BGI_SEQ2000_BGI_3_20180530_LCL5) + '\t' \
		+ str(Quartet_DNA_BGI_T7_WGE_1_20191105_LCL5) + '\t' + str(Quartet_DNA_BGI_T7_WGE_2_20191105_LCL5) + '\t' + str(Quartet_DNA_BGI_T7_WGE_3_20191105_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_ARD_1_20181108_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_2_20181108_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_3_20181108_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_ARD_4_20190111_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_5_20190111_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_ARD_6_20190111_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_BRG_1_20180930_LCL5)  + '\t' + str(Quartet_DNA_ILM_Nova_BRG_2_20180930_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_BRG_3_20180930_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_Nova_WUX_1_20190917_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_WUX_2_20190917_LCL5) + '\t' + str(Quartet_DNA_ILM_Nova_WUX_3_20190917_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_XTen_ARD_1_20170403_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_ARD_2_20170403_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_ARD_3_20170403_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_XTen_NVG_1_20170329_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_NVG_2_20170329_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_NVG_3_20170329_LCL5) + '\t' \
		+ str(Quartet_DNA_ILM_XTen_WUX_1_20170216_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_WUX_2_20170216_LCL5) + '\t' + str(Quartet_DNA_ILM_XTen_WUX_3_20170216_LCL5) + '\n'
		all_sample_outfile.write(outline2)





