from __future__ import division
import pandas as pd
import sys, argparse, os


# input arguments
parser = argparse.ArgumentParser(description="this script is to calculate jaccard index")

parser.add_argument('-i', '--mergedGVCF', type=str, help='merged gVCF txt with only chr, pos, ref, alt and genotypes',  required=True)
parser.add_argument('-prefix', '--prefix', type=str, help='prefix of output file',  required=True)


args = parser.parse_args()
input_dat = args.mergedGVCF
prefix = args.prefix


# output file
output_inter_name = prefix + '.inter.txt'
output_union_name = prefix + '.union.txt'


# input files
dat = pd.read_table(input_dat)

# output files
sample_size = dat.shape[1]-4
inter_number = pd.DataFrame(index=range(sample_size),columns=range(sample_size))
union_number = pd.DataFrame(index=range(sample_size),columns=range(sample_size))

for i in range(sample_size):
    oneSNV_GT = dat.iloc[:,0].astype(str) + '_' + dat.iloc[:,1].astype(str) + '_' + dat.iloc[:,i+4].astype(str)
    print(i+1)
    for j in range(sample_size):
        anotherSNV_GT = dat.iloc[:,0].astype(str) + '_' + dat.iloc[:,1].astype(str) + '_' + dat.iloc[:,j+4].astype(str)
        #remove './.' and '0/0'
        oneSNV_GT = [e for e in oneSNV_GT if './.' not in e]
        oneSNV_GT = [e for e in oneSNV_GT if '0/0' not in e]
        anotherSNV_GT = [e for e in anotherSNV_GT if './.' not in e]
        anotherSNV_GT = [e for e in anotherSNV_GT if '0/0' not in e]
        inter=set(oneSNV_GT).intersection(set(anotherSNV_GT))
        union=set(oneSNV_GT).union(set(anotherSNV_GT))
        inter_number.iloc[i,j] = len(inter)
        union_number.iloc[i,j] = len(union)

inter_number.columns = dat.columns[4:dat.shape[1]]
inter_number.index = dat.columns[4:dat.shape[1]]
union_number.columns = dat.columns[4:dat.shape[1]]
union_number.index = dat.columns[4:dat.shape[1]]

inter_number.to_csv(output_inter_name,sep='\t')
union_number.to_csv(output_union_name,sep='\t')

