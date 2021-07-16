task benchmark {
	File vcf
	File benchmarking_dir
	File ref_dir
	File? qc_bed
	String sample = basename(vcf,".hc.vcf")
	String fasta
	String docker
	String cluster_config
	String disk_size


	command <<<
		set -o pipefail
		set -e
		nt=$(nproc)
		mkdir -p /cromwell_root/tmp
		cp -r ${ref_dir} /cromwell_root/tmp/
		cp -r ${benchmarking_dir} /cromwell_root/tmp/

		export HGREF=/cromwell_root/tmp/reference_data/GRCh38.d1.vd1.fa

		/opt/rtg-tools/dist/rtg-tools-3.10.1-4d58ead/rtg bgzip ${vcf} -c > ${sample}.rtg.vcf.gz
		/opt/rtg-tools/dist/rtg-tools-3.10.1-4d58ead/rtg index -f vcf ${sample}.rtg.vcf.gz

		if [ ${qc_bed} ];then
			if [[ ${sample} =~ "LCL5" ]];then
				/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL5.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f ${qc_bed}--threads $nt -o ${sample} -r ${ref_dir}/${fasta}
		    elif [[ ${sample} =~ "LCL6" ]]; then
		    	/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL6.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f ${qc_bed} --threads $nt -o ${sample} -r ${ref_dir}/${fasta}
	        elif [[ ${sample} =~ "LCL7" ]]; then
	        	/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL7.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f ${qc_bed} --threads $nt -o ${sample} -r ${ref_dir}/${fasta}
		    elif [[ ${sample} =~ "LCL8" ]]; then
				/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL8.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f ${qc_bed} --threads $nt -o ${sample} -r ${ref_dir}/${fasta}
	        else
	        	echo "only for quartet samples"
	        fi
	    else
			if [[ ${sample} =~ "LCL5" ]];then
				/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL5.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f /cromwell_root/tmp/reference_datasets_v202103/Quartet.high.confidence.region.v202103.bed --threads $nt -o ${sample} -r ${ref_dir}/${fasta}
		    elif [[ ${sample} =~ "LCL6" ]]; then
		    	/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL6.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f /cromwell_root/tmp/reference_datasets_v202103/Quartet.high.confidence.region.v202103.bed --threads $nt -o ${sample} -r ${ref_dir}/${fasta}
	        elif [[ ${sample} =~ "LCL7" ]]; then
	        	/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL7.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f /cromwell_root/tmp/reference_datasets_v202103/Quartet.high.confidence.region.v202103.bed --threads $nt -o ${sample} -r ${ref_dir}/${fasta}
		    elif [[ ${sample} =~ "LCL8" ]]; then
				/opt/hap.py/bin/hap.py /cromwell_root/tmp/reference_datasets_v202103/LCL8.high.confidence.calls.vcf ${sample}.rtg.vcf.gz -f /cromwell_root/tmp/reference_datasets_v202103/Quartet.high.confidence.region.v202103.bed --threads $nt -o ${sample} -r ${ref_dir}/${fasta}
	        else
	        	echo "only for quartet samples"	    	
	    fi


	>>>

	runtime {
		docker:docker
		cluster:cluster_config
		systemDisk:"cloud_ssd 40"
		dataDisk:"cloud_ssd " + disk_size + " /cromwell_root/"
	}

	output {
		File rtg_vcf = "${sample}.rtg.vcf.gz"
		File rtg_vcf_index = "${sample}.rtg.vcf.gz.tbi"
		File gzip_vcf = "${sample}.vcf.gz"
		File gzip_vcf_index = "${sample}.vcf.gz.tbi"
		File roc_all_csv = "${sample}.roc.all.csv.gz"
		File roc_indel = "${sample}.roc.Locations.INDEL.csv.gz"
		File roc_indel_pass = "${sample}.roc.Locations.INDEL.PASS.csv.gz"
		File roc_snp = "${sample}.roc.Locations.SNP.csv.gz"
		File roc_snp_pass = "${sample}.roc.Locations.SNP.PASS.csv.gz"
		File summary = "${sample}.summary.csv"
		File extended = "${sample}.extended.csv"
		File metrics = "${sample}.metrics.json.gz"
	}
}