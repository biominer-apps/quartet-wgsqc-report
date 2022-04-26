task rename_vcf {

	File vcf_D5
	File vcf_D6
	File vcf_F7
	File vcf_M8

	String project
	String docker
	String cluster_config
	String disk_size

	command <<<
		mv vcf_D5 ${project}_LCL5.vcf
		mv vcf_D6 ${project}_LCL6.vcf
		mv vcf_F7 ${project}_LCL7.vcf
		mv vcf_M8 ${project}_LCL8.vcf
	>>>

	runtime {
		docker:docker
		cluster:cluster_config
		systemDisk:"cloud_ssd 40"
		dataDisk:"cloud_ssd " + disk_size + " /cromwell_root/"
	}

	output {
		File vcf_D5_renamed = "${project}_LCL5.vcf"
		File vcf_D6_renamed = "${project}_LCL6.vcf"
		File vcf_F7_renamed = "${project}_LCL7.vcf"
		File vcf_M8_renamed = "${project}_LCL8.vcf"
	}
}