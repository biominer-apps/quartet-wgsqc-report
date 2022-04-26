task fastq_screen {
	File read1
	File read2
	File screen_ref_dir
	File fastq_screen_conf
	String docker
	String cluster_config
	String disk_size

	command <<<
		set -o pipefail
		set -e
		nt=$(nproc)
		mkdir -p /cromwell_root/tmp
		cp -r ${screen_ref_dir} /cromwell_root/tmp/
		fastq_screen --aligner bowtie2 --conf ${fastq_screen_conf} --subset 1000000 --threads $nt ${read1}
		fastq_screen --aligner bowtie2 --conf ${fastq_screen_conf} --subset 1000000 --threads $nt ${read2}
	>>>

	runtime {
		docker:docker
		cluster: cluster_config
		systemDisk: "cloud_ssd 40"
		dataDisk: "cloud_ssd " + disk_size + " /cromwell_root/"
	}
	
	output {
		File png1 = sub(basename(read1), "\\.(fastq|fq)\\.gz$", "_screen.png")
		File txt1 = sub(basename(read1), "\\.(fastq|fq)\\.gz$", "_screen.txt")
		File html1 = sub(basename(read1), "\\.(fastq|fq)\\.gz$", "_screen.html")
		File png2 = sub(basename(read2), "\\.(fastq|fq)\\.gz$", "_screen.png")
		File txt2 = sub(basename(read2), "\\.(fastq|fq)\\.gz$", "_screen.txt")
		File html2 = sub(basename(read2), "\\.(fastq|fq)\\.gz$", "_screen.html")
	}
}