import pandas as pd
import sys, argparse, os


# input arguments
parser = argparse.ArgumentParser(description="This script is to get column sum of all variants in SV breakpoints flanking region")

parser.add_argument('-file', '--file', type=str, help='The bed annotated file',  required=True)
parser.add_argument('-prefix', '--prefix', type=str, help='The prefix of output file',  required=True)


args = parser.parse_args()
file = args.file
prefix = args.prefix


dat = pd.read_table(file,header=None)
dat_sub = dat.iloc[:,5:]
dat_sum = pd.DataFrame(dat_sub.sum())
dat_sum.columns = [prefix]
file_name = prefix + '.sum.txt'
dat_sum.to_csv(file_name,index=0)