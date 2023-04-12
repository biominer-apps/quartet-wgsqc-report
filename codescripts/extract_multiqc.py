import json
import pandas as pd
import sys, argparse, os

parser = argparse.ArgumentParser(description="This script is to get information from multiqc")

parser.add_argument('-fastqc_qualimap', '--fastqc_qualimap', type=str, help='multiqc_general_stats.txt',  required=True)
parser.add_argument('-fastqc', '--fastqc', type=str, help='multiqc_fastqc.txt',  required=True)
parser.add_argument('-fastqscreen', '--fastqscreen', type=str, help='multiqc_fastq_screen.txt',  required=True)
parser.add_argument('-hap', '--happy', type=str, help='multiqc_happy_data.json',  required=True)

args = parser.parse_args()

# Rename input:
fastqc_qualimap_file = args.fastqc_qualimap
fastqc_file = args.fastqc
fastqscreen_file = args.fastqscreen
hap_file = args.happy


# fastqc and qualimap
dat = pd.read_table(fastqc_qualimap_file)

fastqc = dat.loc[:, dat.columns.str.startswith('FastQC')]
fastqc.insert(loc=0, column='Sample', value=dat['Sample'])
fastqc_stat = fastqc.dropna()

# qulimap
qualimap = dat.loc[:, dat.columns.str.startswith('QualiMap')]
qualimap.insert(loc=0, column='Sample', value=dat['Sample'])
qualimap_stat = qualimap.dropna()

# fastqc
dat = pd.read_table(fastqc_file)

fastqc_module = dat.loc[:, "per_base_sequence_quality":"kmer_content"]
fastqc_module.insert(loc=0, column='Sample', value=dat['Sample'])
fastqc_all = pd.merge(fastqc_stat,fastqc_module,  how='outer', left_on=['Sample'], right_on = ['Sample'])

# fastqscreen
dat = pd.read_table(fastqscreen_file)
fastqscreen = dat.loc[:, dat.columns.str.endswith('percentage')]
dat['Sample'] = [i.replace('_screen','') for i in dat['Sample']]
fastqscreen.insert(loc=0, column='Sample', value=dat['Sample'])

# benchmark
with open(hap_file) as hap_json:
	happy = json.load(hap_json)
dat =pd.DataFrame.from_records(happy)
dat = dat.loc[:, dat.columns.str.endswith('ALL')]
dat_transposed = dat.T
benchmark = dat_transposed.loc[:,['sample_id','METRIC.Precision','METRIC.Recall']]
benchmark['sample_id'] = benchmark.index
benchmark.columns = ['Sample','Precision','Recall']

#output
fastqc_all.to_csv('fastqc.final.result.txt',sep="\t",index=0)
fastqscreen.to_csv('fastqscreen.final.result.txt',sep="\t",index=0)
qualimap_stat.to_csv('qualimap.final.result.txt',sep="\t",index=0)
benchmark.to_csv('benchmark.final.result.txt',sep="\t",index=0)






