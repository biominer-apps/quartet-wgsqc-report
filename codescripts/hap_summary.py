import pandas as pd
import sys, argparse, os

parser = argparse.ArgumentParser(description="This script is to get information from hap")
parser.add_argument('-hap', '--happy', type=str, help='hap.py table',  required=True)
parser.add_argument('-name', '--name', type=str, help='hap.py table',  required=True)

args = parser.parse_args()

hap_file = args.happy
name = args.name

dat = pd.read_table(hap_file)
dat['QUERY.TP'] = dat['QUERY.TOTAL'].astype(int) - dat['QUERY.UNK'].astype(int) - dat['QUERY.FP'].astype(int)
dat['QUERY'] = dat['QUERY.TOTAL'].astype(int) - dat['QUERY.UNK'].astype(int)
indel = dat[['INDEL' in s for s in dat['Type']]]
snv = dat[['SNP' in s for s in dat['Type']]]
indel.reset_index(drop=True, inplace=True)
snv.reset_index(drop=True, inplace=True)
benchmark = pd.concat([snv, indel], axis=1)
benchmark = benchmark[[ 'QUERY.TOTAL', 'QUERY','QUERY.TP','QUERY.FP','TRUTH.FN','METRIC.Precision', 'METRIC.Recall','METRIC.F1_Score']]
benchmark.columns = ['SNV number','INDEL number','SNV query','INDEL query','SNV TP','INDEL TP','SNV FP','INDEL FP','SNV FN','INDEL FN','SNV precision','INDEL precision','SNV recall','INDEL recall','SNV F1','INDEL F1']
benchmark = benchmark[['SNV number','INDEL number','SNV query','INDEL query','SNV TP','INDEL TP','SNV FP','INDEL FP','SNV FN','INDEL FN','SNV precision','INDEL precision','SNV recall','INDEL recall','SNV F1','INDEL F1']]
benchmark['SNV precision'] = benchmark['SNV precision'].astype(float)
benchmark['INDEL precision'] = benchmark['INDEL precision'].astype(float)
benchmark['SNV recall'] = benchmark['SNV recall'].astype(float)
benchmark['INDEL recall'] = benchmark['INDEL recall'].astype(float)
benchmark['SNV F1'] = benchmark['SNV F1'].astype(float)
benchmark['INDEL F1'] = benchmark['INDEL F1'].astype(float)
benchmark = benchmark.round(2)

name_array = name.split("_")
LCL5_1 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL5_1" + "_" + name_array[5]
LCL5_2 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL5_2" + "_" + name_array[5]
LCL5_3 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL5_3" + "_" + name_array[5]

LCL6_1 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL6_1" + "_" + name_array[5]
LCL6_2 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL6_2" + "_" + name_array[5]
LCL6_3 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL6_3" + "_" + name_array[5]

LCL7_1 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL7_1" + "_" + name_array[5]
LCL7_2 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL7_2" + "_" + name_array[5]
LCL7_3 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL7_3" + "_" + name_array[5]

LCL8_1 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL8_1" + "_" + name_array[5]
LCL8_2 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL8_2" + "_" + name_array[5]
LCL8_3 = name_array[0] + "_" + name_array[1] + "_" + name_array[2] + "_" + name_array[3] + "_"  + name_array[4] + "_" + "LCL8_3" + "_" + name_array[5]

benchmark.insert(loc=0, column='Sample', value=[LCL5_1,LCL5_2,LCL5_3,LCL6_1,LCL6_2,LCL6_3,LCL7_1,LCL7_2,LCL7_3,LCL8_1,LCL8_2,LCL8_3])
benchmark.to_csv('variants.calling.qc.txt',sep="\t",index=0)