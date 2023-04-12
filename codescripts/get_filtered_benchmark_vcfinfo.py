from __future__ import division
import pandas as pd
import sys, argparse, os
import fileinput


# input arguments
parser = argparse.ArgumentParser(description="this script is to get filtered and benchmark vcf info")

parser.add_argument('-filtered', '--filtered', type=str, help='filtered position',  required=True)
parser.add_argument('-benchmark', '--benchmark', type=str, help='benchmark position',  required=True)
parser.add_argument('-vcf', '--vcf', type=str, help='one specific vcf',  required=True)
parser.add_argument('-filename', '--filename', type=str, help='output file name',  required=True)


args = parser.parse_args()
filtered = args.filtered
benchmark = args.benchmark
vcf = args.vcf
filename = args.filename


# output file
filtered_filename = filename + '.filtered.txt'
benchmark_filename = filename + '.benchmark.txt'

# input files
filtered_dat = pd.read_table(filtered,header=None)
benchmark_dat = pd.read_table(benchmark,header=None)
vcf_dat = pd.read_table(vcf)

filtered_merged_df = pd.merge(filtered_dat, vcf_dat,  how='inner',left_on=[0,1], right_on = ['#CHROM','POS'])
benchmark_merged_df = pd.merge(benchmark_dat,vcf_dat, how='inner',left_on=[0,1], right_on = ['#CHROM','POS'])

filtered_merged_df.to_csv(filtered_filename,sep='\t',index=False)
benchmark_merged_df.to_csv(benchmark_filename,sep='\t',index=False)
