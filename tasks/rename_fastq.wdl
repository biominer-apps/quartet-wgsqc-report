task rename_fastq {

	File fastq_1_D5
	File fastq_1_D6
	File fastq_1_F7
	File fastq_1_M8

	File fastq_2_D5
	File fastq_2_D6
	File fastq_2_F7
	File fastq_2_M8

	String project
	String docker
	String cluster_config
	String disk_size

	command <<<
		mv fastq_1_D5 ${project}_LCL5.R1.fastq.gz
		mv fastq_1_D6 ${project}_LCL6.R1.fastq.gz
		mv fastq_1_F7 ${project}_LCL7.R1.fastq.gz
		mv fastq_1_M8 ${project}_LCL8.R1.fastq.gz
		mv fastq_2_D5 ${project}_LCL5.R2.fastq.gz
		mv fastq_2_D6 ${project}_LCL6.R2.fastq.gz
		mv fastq_2_F7 ${project}_LCL7.R2.fastq.gz
		mv fastq_2_M8 ${project}_LCL8.R2.fastq.gz

	>>>

	runtime {
		docker:docker
		cluster:cluster_config
		systemDisk:"cloud_ssd 40"
		dataDisk:"cloud_ssd " + disk_size + " /cromwell_root/"
	}

	output {
		File fastq_1_D5_renamed = "${project}_LCL5.R1.fastq.gz"
		File fastq_1_D6_renamed = "${project}_LCL6.R1.fastq.gz"
		File fastq_1_F7_renamed = "${project}_LCL7.R1.fastq.gz"
		File fastq_1_M8_renamed = "${project}_LCL8.R1.fastq.gz"
		File fastq_2_D5_renamed = "${project}_LCL5.R2.fastq.gz"
		File fastq_2_D6_renamed = "${project}_LCL6.R2.fastq.gz"
		File fastq_2_F7_renamed = "${project}_LCL7.R2.fastq.gz"
		File fastq_2_M8_renamed = "${project}_LCL8.R2.fastq.gz"
	}
}