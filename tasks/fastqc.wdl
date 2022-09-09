task fastqc {
	File read1
	File read2
	String docker
	String project
	String sample
	String cluster_config
	String disk_size

	command <<<
		set -o pipefail
		set -e
		nt=$(nproc)
		cp ${read1} ${project}_${sample}_R1.fastq.gz
		cp ${read2} ${project}_${sample}_R2.fastq.gz
		fastqc -t $nt -o ./ ${project}_${sample}_R1.fastq.gz
		fastqc -t $nt -o ./ ${project}_${sample}_R2.fastq.gz
	>>>

	runtime {
		docker:docker
    	cluster: cluster_config
    	systemDisk: "cloud_ssd 40"
    	dataDisk: "cloud_ssd " + disk_size + " /cromwell_root/"
	}
	output {
		File read1_html = "${project}_${sample}_R1_fastqc.html"
		File read1_zip = "${project}_${sample}_R1_fastqc.zip"
		File read2_html = "${project}_${sample}_R2_fastqc.html"
		File read2_zip = "${project}_${sample}_R2_fastqc.html"
	}
}