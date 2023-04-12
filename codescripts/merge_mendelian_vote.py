import pandas as pd
import sys, argparse, os

men = pd.read_table(sys.argv[1],header=None)
vote = pd.read_table(sys.argv[2],low_memory=False)
mut = pd.read_table(sys.argv[3],header=None)

merged_df = pd.merge(vote, men,  how='inner', left_on=['CHROM','POS'], right_on = [0,1])
merged_df['mendelian_check'] = 'MIE'
merged_df.loc[merged_df[2]=='1:1:1','mendelian_check'] = 'MP'
sub = merged_df[['CHROM','POS','LCL5_detected_num','mendelian_check',2]]
sub.columns=['CHROM','POS','detected_num','mendelian','detail']
genotype_sub = pd.merge(sub, mut,  how='inner', left_on=["CHROM","POS"], right_on = [0,1])
genotype_sub = genotype_sub[['CHROM','POS','detected_num','mendelian','detail',2,3]]
genotype_sub.to_csv(sys.argv[4],header=0,sep="\t",index=0)