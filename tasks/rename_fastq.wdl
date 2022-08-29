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
		mv fastq_1_D5 ${project}_LCL5_R1.fastq.gz
		mv fastq_1_D6 ${project}_LCL6_R1.fastq.gz
		mv fastq_1_F7 ${project}_LCL7_R1.fastq.gz
		mv fastq_1_M8 ${project}_LCL8_R1.fastq.gz
		mv fastq_2_D5 ${project}_LCL5_R2.fastq.gz
		mv fastq_2_D6 ${project}_LCL6_R2.fastq.gz
		mv fastq_2_F7 ${project}_LCL7_R2.fastq.gz
		mv fastq_2_M8 ${project}_LCL8_R2.fastq.gz

	>>>

	runtime {
		docker:docker
		cluster:cluster_config
		systemDisk:"cloud_ssd 40"
		dataDisk:"cloud_ssd " + disk_size + " /cromwell_root/"
	}

	output {
		File fastq_1_D5_renamed = "${project}_LCL5_R1.fastq.gz"
		File fastq_1_D6_renamed = "${project}_LCL6_R1.fastq.gz"
		File fastq_1_F7_renamed = "${project}_LCL7_R1.fastq.gz"
		File fastq_1_M8_renamed = "${project}_LCL8_R1.fastq.gz"
		File fastq_2_D5_renamed = "${project}_LCL5_R2.fastq.gz"
		File fastq_2_D6_renamed = "${project}_LCL6_R2.fastq.gz"
		File fastq_2_F7_renamed = "${project}_LCL7_R2.fastq.gz"
		File fastq_2_M8_renamed = "${project}_LCL8_R2.fastq.gz"
	}
}