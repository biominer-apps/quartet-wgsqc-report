import "./tasks/mapping.wdl" as mapping
import "./tasks/Dedup.wdl" as Dedup
import "./tasks/qualimap.wdl" as qualimap
import "./tasks/deduped_Metrics.wdl" as deduped_Metrics
import "./tasks/sentieon.wdl" as sentieon
import "./tasks/Realigner.wdl" as Realigner
import "./tasks/BQSR.wdl" as BQSR
import "./tasks/Haplotyper.wdl" as Haplotyper
import "./tasks/benchmark.wdl" as benchmark
import "./tasks/multiqc.wdl" as multiqc
import "./tasks/merge_sentieon_metrics.wdl" as merge_sentieon_metrics
import "./tasks/extract_tables.wdl" as extract_tables
import "./tasks/mendelian.wdl" as mendelian
import "./tasks/merge_mendelian.wdl" as merge_mendelian
import "./tasks/quartet_mendelian.wdl" as quartet_mendelian
import "./tasks/fastqc.wdl" as fastqc
import "./tasks/fastqscreen.wdl" as fastqscreen
import "./tasks/D5_D6.wdl" as D5_D6
import "./tasks/merge_family.wdl" as merge_family


workflow {{ project_name }} {

	File? fastq_1_D5
	File? fastq_1_D6
	File? fastq_1_F7
	File? fastq_1_M8

	File? fastq_2_D5
	File? fastq_2_D6
	File? fastq_2_F7
	File? fastq_2_M8

	File? vcf_D5
	File? vcf_D6
	File? vcf_F7
	File? vcf_M8

	File? bed

	String SENTIEON_INSTALL_DIR
	String SENTIEON_LICENSE
	String SENTIEONdocker
	String FASTQCdocker
	String FASTQSCREENdocker
	String QUALIMAPdocker
	String BENCHMARKdocker
	String MENDELIANdocker
	String DIYdocker
	String MULTIQCdocker

	String fasta
	File ref_dir
	File dbmills_dir
	String db_mills
	File dbsnp_dir
	String dbsnp

	File screen_ref_dir
	File fastq_screen_conf
	File benchmarking_dir

	String project

	String disk_size
	String BIGcluster_config
	String SMALLcluster_config

	
	if (fastq_1_D5!= "") {

	#######################
	### D5 fastq to vcf ###
    #######################

		call mapping.mapping as mapping_D5 {
			input: 
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			SENTIEON_LICENSE=SENTIEON_LICENSE,
			group="D5",
			sample="D5",
			pl="ILLUMINAL",
			fasta=fasta,
			ref_dir=ref_dir,
			fastq_1=fastq_1_D5,
			fastq_2=fastq_2_D5,
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call fastqc.fastqc as fastqc_D5 {
			input:
			read1=fastq_1_D5,
			read2=fastq_2_D5,
			docker=FASTQCdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call fastqscreen.fastq_screen as fastqscreen_D5 {
			input:
			read1=fastq_1_D5,
			read2=fastq_2_D5,
			screen_ref_dir=screen_ref_dir,
			fastq_screen_conf=fastq_screen_conf,
			docker=FASTQSCREENdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call Dedup.Dedup as Dedup_D5 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			sorted_bam=mapping.sorted_bam,
			sorted_bam_index=mapping.sorted_bam_index,
			sample="D5",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call qualimap.qualimap as qualimap_D5 {
			input:
			bam=Dedup.Dedup_bam,
			bai=Dedup.Dedup_bam_index,
			docker=QUALIMAPdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}		

		call deduped_Metrics.deduped_Metrics as deduped_Metrics_D5 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			sample="D5",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call sentieon.sentieon as sentieon_D5 {
			input:
			quality_yield=deduped_Metrics.deduped_QualityYield,
			wgs_metrics_algo=deduped_Metrics.deduped_wgsmetrics,
			aln_metrics=deduped_Metrics.dedeuped_aln_metrics,
			is_metrics=deduped_Metrics.deduped_is_metrics,
			sample="D5",
			docker=SENTIEONdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size		
		}

		call Realigner.Realigner as Realigner_D5 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			sample="D5",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call BQSR.BQSR as BQSR_D5 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			realigned_bam=Realigner.realigner_bam,
			realigned_bam_index=Realigner.realigner_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			dbsnp=dbsnp,
			dbsnp_dir=dbsnp_dir,
			sample="D5",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call Haplotyper.Haplotyper as Haplotyper_D5 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			recaled_bam=BQSR.recaled_bam,
			recaled_bam_index=BQSR.recaled_bam_index,
			sample="D5",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_D5 {
			input:
			vcf=Haplotyper_D5.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_D5 {
			input:
			vcf=filter_vcf_bed_D5.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_D5.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}		

	#######################
	### D6 fastq to vcf ###
    #######################
	
		call mapping.mapping as mapping_D6 {
			input: 
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			SENTIEON_LICENSE=SENTIEON_LICENSE,
			group="D6",
			sample="D6",
			pl="ILLUMINAL",
			fasta=fasta,
			ref_dir=ref_dir,
			fastq_1=fastq_1_D6,
			fastq_2=fastq_2_D6,
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call fastqc.fastqc as fastqc_D6 {
			input:
			read1=fastq_1_D6,
			read2=fastq_2_D6,
			docker=FASTQCdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call fastqscreen.fastq_screen as fastqscreen_D6 {
			input:
			read1=fastq_1_D6,
			read2=fastq_2_D6,
			screen_ref_dir=screen_ref_dir,
			fastq_screen_conf=fastq_screen_conf,
			docker=FASTQSCREENdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call Dedup.Dedup as Dedup_D6 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			sorted_bam=mapping.sorted_bam,
			sorted_bam_index=mapping.sorted_bam_index,
			sample="D6",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call qualimap.qualimap as qualimap_D6 {
			input:
			bam=Dedup.Dedup_bam,
			bai=Dedup.Dedup_bam_index,
			docker=QUALIMAPdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}		

		call deduped_Metrics.deduped_Metrics as deduped_Metrics_D6 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			sample="D6",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call sentieon.sentieon as sentieon_D6 {
			input:
			quality_yield=deduped_Metrics.deduped_QualityYield,
			wgs_metrics_algo=deduped_Metrics.deduped_wgsmetrics,
			aln_metrics=deduped_Metrics.dedeuped_aln_metrics,
			is_metrics=deduped_Metrics.deduped_is_metrics,
			sample="D6",
			docker=SENTIEONdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size		
		}

		call Realigner.Realigner as Realigner_D6 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			sample="D6",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call BQSR.BQSR as BQSR_D6 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			realigned_bam=Realigner.realigner_bam,
			realigned_bam_index=Realigner.realigner_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			dbsnp=dbsnp,
			dbsnp_dir=dbsnp_dir,
			sample="D6",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call Haplotyper.Haplotyper as Haplotyper_D6 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			recaled_bam=BQSR.recaled_bam,
			recaled_bam_index=BQSR.recaled_bam_index,
			sample="D6",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_D6 {
			input:
			vcf=Haplotyper_D6.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_D6 {
			input:
			vcf=filter_vcf_bed_D6.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_D6.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}


	#######################
	### F7 fastq to vcf ###
    #######################
	
		call mapping.mapping as mapping_F7 {
			input: 
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			SENTIEON_LICENSE=SENTIEON_LICENSE,
			group="F7",
			sample="F7",
			pl="ILLUMINAL",
			fasta=fasta,
			ref_dir=ref_dir,
			fastq_1=fastq_1_F7,
			fastq_2=fastq_2_F7,
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call fastqc.fastqc as fastqc_F7 {
			input:
			read1=fastq_1_F7,
			read2=fastq_2_F7,
			docker=FASTQCdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call fastqscreen.fastq_screen as fastqscreen_F7 {
			input:
			read1=fastq_1_F7,
			read2=fastq_2_F7,
			screen_ref_dir=screen_ref_dir,
			fastq_screen_conf=fastq_screen_conf,
			docker=FASTQSCREENdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call Dedup.Dedup as Dedup_F7 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			sorted_bam=mapping.sorted_bam,
			sorted_bam_index=mapping.sorted_bam_index,
			sample="F7",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call qualimap.qualimap as qualimap_F7 {
			input:
			bam=Dedup.Dedup_bam,
			bai=Dedup.Dedup_bam_index,
			docker=QUALIMAPdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}		

		call deduped_Metrics.deduped_Metrics as deduped_Metrics_F7 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			sample="F7",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call sentieon.sentieon as sentieon_F7 {
			input:
			quality_yield=deduped_Metrics.deduped_QualityYield,
			wgs_metrics_algo=deduped_Metrics.deduped_wgsmetrics,
			aln_metrics=deduped_Metrics.dedeuped_aln_metrics,
			is_metrics=deduped_Metrics.deduped_is_metrics,
			sample="F7",
			docker=SENTIEONdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size		
		}

		call Realigner.Realigner as Realigner_F7 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			sample="F7",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call BQSR.BQSR as BQSR_F7 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			realigned_bam=Realigner.realigner_bam,
			realigned_bam_index=Realigner.realigner_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			dbsnp=dbsnp,
			dbsnp_dir=dbsnp_dir,
			sample="F7",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call Haplotyper.Haplotyper as Haplotyper_F7 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			recaled_bam=BQSR.recaled_bam,
			recaled_bam_index=BQSR.recaled_bam_index,
			sample="F7",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_F7 {
			input:
			vcf=Haplotyper_F7.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_F7 {
			input:
			vcf=filter_vcf_bed_F7.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_F7.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

	#######################
	### M8 fastq to vcf ###
    #######################
	
		call mapping.mapping as mapping_M8 {
			input: 
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			SENTIEON_LICENSE=SENTIEON_LICENSE,
			group="M8",
			sample="M8",
			pl="ILLUMINAL",
			fasta=fasta,
			ref_dir=ref_dir,
			fastq_1=fastq_1_M8,
			fastq_2=fastq_2_M8,
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call fastqc.fastqc as fastqc_M8 {
			input:
			read1=fastq_1_M8,
			read2=fastq_2_M8,
			docker=FASTQCdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call fastqscreen.fastq_screen as fastqscreen_M8 {
			input:
			read1=fastq_1_M8,
			read2=fastq_2_M8,
			screen_ref_dir=screen_ref_dir,
			fastq_screen_conf=fastq_screen_conf,
			docker=FASTQSCREENdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call Dedup.Dedup as Dedup_M8 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			sorted_bam=mapping.sorted_bam,
			sorted_bam_index=mapping.sorted_bam_index,
			sample="M8",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call qualimap.qualimap as qualimap_M8 {
			input:
			bam=Dedup.Dedup_bam,
			bai=Dedup.Dedup_bam_index,
			docker=QUALIMAPdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}		

		call deduped_Metrics.deduped_Metrics as deduped_Metrics_M8 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			sample="M8",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call sentieon.sentieon as sentieon_M8 {
			input:
			quality_yield=deduped_Metrics.deduped_QualityYield,
			wgs_metrics_algo=deduped_Metrics.deduped_wgsmetrics,
			aln_metrics=deduped_Metrics.dedeuped_aln_metrics,
			is_metrics=deduped_Metrics.deduped_is_metrics,
			sample="M8",
			docker=SENTIEONdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size		
		}

		call Realigner.Realigner as Realigner_M8 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			Dedup_bam=Dedup.Dedup_bam,
			Dedup_bam_index=Dedup.Dedup_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			sample="M8",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call BQSR.BQSR as BQSR_M8 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			realigned_bam=Realigner.realigner_bam,
			realigned_bam_index=Realigner.realigner_bam_index,
			db_mills=db_mills,
			dbmills_dir=dbmills_dir,
			dbsnp=dbsnp,
			dbsnp_dir=dbsnp_dir,
			sample="M8",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call Haplotyper.Haplotyper as Haplotyper_M8 {
			input:
			SENTIEON_INSTALL_DIR=SENTIEON_INSTALL_DIR,
			fasta=fasta,
			ref_dir=ref_dir,
			recaled_bam=BQSR.recaled_bam,
			recaled_bam_index=BQSR.recaled_bam_index,
			sample="M8",
			docker=SENTIEONdocker,
			disk_size=disk_size,
			cluster_config=BIGcluster_config
		}

		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_M8 {
			input:
			vcf=Haplotyper_M8.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_M8 {
			input:
			vcf=filter_vcf_bed_M8.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_M8.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}
	}

	#######################
	###     merge qc    ###
    #######################

	    Array[File] fastqc_read1_zip = [fastqc_D5.read1_zip, fastqc_D6.read1_zip, fastqc_F7.read1_zip, fastqc_M8.read1_zip]

	    Array[File] fastqc_read2_zip = [fastqc_D5.read2_zip, fastqc_D6.read2_zip, fastqc_F7.read2_zip, fastqc_M8.read2_zip]

	    Array[File] fastqscreen_txt1 = [fastqscreen_D5.txt1, fastqscreen_D6.txt1, fastqscreen_F7.txt1, fastqscreen_M8.txt1]

	    Array[File] fastqscreen_txt2 = [fastqscreen_D5.txt2, fastqscreen_D6.txt2, fastqscreen_F7.txt2, fastqscreen_M8.txt2]

	    Array[File] benchmark_summary = [benchmark_D5.summary, benchmark_D6.summary, benchmark_F7.summary, benchmark_M8.summary]

	    Array[File] qualimap_zip = [qualimap_D5.zip, qualimap_D6.zip, qualimap_F7.zip, qualimap_M8.zip]


		call multiqc.multiqc as multiqc {
			input:
			read1_zip=fastqc_read1_zip,
			read2_zip=fastqc_read2_zip,
			txt1=fastqscreen_txt1,
			txt2=fastqscreen_txt2,
			summary=benchmark_summary,
			zip=qualimap_zip,
			docker=MULTIQCdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size
		}


		Array[File] sentieon_quality_yield_header = [sentieon_D5.quality_yield_header, sentieon_D6.quality_yield_header, sentieon_F7.quality_yield_header, sentieon_M8.quality_yield_header]

		Array[File] sentieon_wgs_metrics_algo_header = [sentieon_D5.wgs_metrics_algo_header, sentieon_D6.wgs_metrics_algo_header, sentieon_F7.wgs_metrics_algo_header, sentieon_M8.wgs_metrics_algo_header]

		Array[File] sentieon_aln_metrics_header = [sentieon_D5.aln_metrics_header, sentieon_D6.aln_metrics_header, sentieon_F7.aln_metrics_header, sentieon_M8.aln_metrics_header]

		Array[File] sentieon_is_metrics_header = [sentieon_D5.is_metrics_header, sentieon_D6.is_metrics_header, sentieon_F7.is_metrics_header, sentieon_M8.is_metrics_header]

		Array[File] sentieon_quality_yield_data = [sentieon_D5.quality_yield_data, sentieon_D6.quality_yield_data, sentieon_F7.quality_yield_data, sentieon_M8.quality_yield_data]

		Array[File] sentieon_wgs_metrics_algo_data = [sentieon_D5.wgs_metrics_algo_data, sentieon_D6.wgs_metrics_algo_data, sentieon_F7.wgs_metrics_algo_data, sentieon_M8.wgs_metrics_algo_data]

		Array[File] sentieon_aln_metrics_data = [sentieon_D5.aln_metrics_data, sentieon_D6.aln_metrics_data, sentieon_F7.aln_metrics_data, sentieon_M8.aln_metrics_data]

		Array[File] sentieon_is_metrics_data = [sentieon_D5.is_metrics_data, sentieon_D6.is_metrics_data, sentieon_F7.is_metrics_data, sentieon_M8.is_metrics_data]

		call merge_sentieon_metrics.merge_sentieon_metrics as merge_sentieon_metrics {
			input:
			quality_yield_header=sentieon_quality_yield_header,
			wgs_metrics_algo_header=sentieon_wgs_metrics_algo_header,
			aln_metrics_header=sentieon_aln_metrics_header,
			is_metrics_header=sentieon_is_metrics_header,
			quality_yield_data=sentieon_quality_yield_data,
			wgs_metrics_algo_data=sentieon_wgs_metrics_algo_data,
			aln_metrics_data=sentieon_aln_metrics_data,
			is_metrics_data=sentieon_is_metrics_data,
			project=project,
			docker=MULTIQCdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size	
		}

		call extract_tables.extract_tables as extract_tables {
			input:
			quality_yield_summary=merge_sentieon_metrics.quality_yield_summary,
			wgs_metrics_summary=merge_sentieon_metrics.wgs_metrics_summary,
			aln_metrics_summary=merge_sentieon_metrics.aln_metrics_summary,
			is_metrics_summary=merge_sentieon_metrics.is_metrics_summary,
			fastqc=multiqc.fastqc,
			fastqscreen=multiqc.fastqscreen,
			hap=multiqc.hap,
			project=project,
			docker=DIYdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size
		}
	}

	############################
	##  vcf input preprocess  ##
	############################
	if (vcf_D5!= "") {
		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_D5 {
			input:
			vcf=Haplotyper_D5.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_D5 {
			input:
			vcf=filter_vcf_bed_D5.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_D5.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}		

		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_D6 {
			input:
			vcf=Haplotyper_D6.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_D6 {
			input:
			vcf=filter_vcf_bed_D6.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_D6.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_F7 {
			input:
			vcf=Haplotyper_F7.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_F7 {
			input:
			vcf=filter_vcf_bed_F7.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_F7.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

		call filter_vcf_bed.filter_vcf_bed as filter_vcf_bed_M8 {
			input:
			vcf=Haplotyper_M8.vcf,
			bed=bed,
			benchmark_region=benchmark_region,
			project=project,
			docker=docker,
			cluster_config=cluster_config,
			disk_size=disk_size			
		}

		call benchmark.benchmark as benchmark_M8 {
			input:
			vcf=filter_vcf_bed_M8.filterd_vcf,
			benchmarking_dir=benchmarking_dir,
			ref_dir=ref_dir,
			qc_bed=filter_vcf_bed_M8.filtered_bed,
			fasta=fasta,
			docker=BENCHMARKdocker,
			cluster_config=BIGcluster_config,
			disk_size=disk_size
		}

	    Array[File] benchmark_summary = [benchmark_D5.summary, benchmark_D6.summary, benchmark_F7.summary, benchmark_M8.summary]

	    #### multiqc

		call multiqc.multiqc as multiqc {
			input:
			summary=benchmark_summary,
			docker=MULTIQCdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size
		}	    

	    #### extract table

		call extract_tables.extract_tables as extract_tables {
			input:
			hap=multiqc.hap,
			project=project,
			docker=DIYdocker,
			cluster_config=SMALLcluster_config,
			disk_size=disk_size
		}
	}

	########################
	###     mendelian    ###
    ########################

	call merge_family.merge_family as merge_family {
		input:
		D5_vcf=benchmark_D5.rtg_vcf,
		D6_vcf=benchmark_D6.rtg_vcf,
		F7_vcf=benchmark_F7.rtg_vcf,
		M8_vcf=benchmark_M8.rtg_vcf,
		D5_vcf_tbi=benchmark_D5.rtg_vcf_index,
		D6_vcf_tbi=benchmark_D6.rtg_vcf_index,
		F7_vcf_tbi=benchmark_F7.rtg_vcf_index,
		M8_vcf_tbi=benchmark_M8.rtg_vcf_index,
		project=project,
		docker=DIYdocker,
		cluster_config=SMALLcluster_config,
		disk_size=disk_size,
	}

	call mendelian.mendelian as mendelian {
		input:
		family_vcf=family_vcfs[idx],
		ref_dir=ref_dir,
		fasta=fasta,
		docker=MENDELIANdocker,
		cluster_config=BIGcluster_config,
		disk_size=disk_size		
	}

	call merge_mendelian.merge_mendelian as merge_mendelian {
		input:
		D5_trio_vcf=mendelian.D5_trio_vcf,
		D6_trio_vcf=mendelian.D6_trio_vcf,
		family_vcf=family_vcfs[idx],
		docker=DIYdocker,
		cluster_config=SMALLcluster_config,
		disk_size=disk_size
	}	
}


