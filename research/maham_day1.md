# Cancer Variant Calling and Annotation Pipeline

## Day 1 Research

**Team Member:** Maham  
**Project Type:** Python  
**Research Phase:** Week 1 - Day 1  
**Date:** 16 August 2026

---

# 1. Sequencing Basics

## A. DNA Sequencing

### What is DNA sequencing?

DNA sequencing is basically the process of finding the order of bases in DNA: A, T, C and G. Modern sequencing machines usually break DNA into many small pieces, read those pieces, and produce millions of short sequences called reads.

### Why is sequencing used in cancer genomics?

Cancer cells can develop genetic changes that help them grow and survive. By sequencing a tumor, we can look for these changes. Comparing the tumor with a normal sample from the same person can also help identify mutations that are specific to the tumor.

### What kind of data does sequencing produce?

The main raw output is a large number of short DNA reads along with quality information for each base. This raw sequencing data is commonly stored in FASTQ files.

### Source

- EMBL-EBI — High-throughput sequencing and cancer genomics
- Galaxy Training Network — Sequence analysis resources

---

## B. FASTQ

### What is FASTQ?

FASTQ is a file format used to store raw sequencing reads together with their quality scores. It is normally one of the first file types used in a sequencing pipeline.

### What does a FASTQ file contain?

Each read normally has four lines:

- Line 1: Read identifier
- Line 2: DNA sequence
- Line 3: `+` separator
- Line 4: Quality scores

The quality scores give an idea of how confident the sequencing machine was about each base.

### What are sequencing reads?

A sequencing read is a short piece of DNA that has been read by the sequencing machine. A sequencing experiment can produce millions of these reads.

### Where does FASTQ appear in our pipeline?

FASTQ is the starting point of our basic workflow:

**FASTQ → Alignment → BAM → Variant Calling → VCF**

### Source

- Galaxy Training Network — FASTQ format
- EMBL-EBI — Sequencing experiments

---

## C. BAM

### What is BAM?

BAM stands for Binary Alignment/Map. It is a compressed binary file format used to store sequencing reads together with information about where those reads align to a reference genome.

### Why do we align sequencing reads?

The reads in a FASTQ file do not initially tell us where they came from in the genome. Alignment compares the reads with a reference genome and finds their likely positions.

### How is BAM related to alignment?

After the reads are aligned, the alignment information can be stored in a BAM file. So, BAM is one of the main outputs of the alignment stage.

### Where does BAM appear in our pipeline?

**FASTQ → Alignment → BAM**

The BAM file is then used by downstream tools for variant calling.

### Source

- SAMtools / GA4GH — SAM/BAM format specifications

---

## D. VCF

### What is VCF?

VCF stands for Variant Call Format. It is a standard file format used to store genetic variants identified during variant calling.

### What information does a VCF contain?

A VCF can contain information such as:

- Chromosome
- Position
- Reference allele
- Alternative allele
- Quality score
- Filter status
- Sample information
- Other information about the variant

### Why is VCF important after variant calling?

VCF contains the variants identified by the variant caller. After this, we can filter the variants and add annotation information to understand which genes or biological effects they may be associated with.

### Basic flow

**FASTQ → Alignment → BAM → Variant Calling → VCF**

This is the basic flow we are trying to understand for our cancer variant-calling project.

### Source

- NCI Genomic Data Commons — VCF documentation
- SAMtools / GA4GH — VCF specifications

---

# 2. Existing Projects

## Project 1 — GATK / Mutect2

### What is GATK?

GATK stands for Genome Analysis Toolkit. It is a collection of tools developed for analyzing high-throughput sequencing data, especially for variant discovery and genotyping.

### What is Mutect2?

Mutect2 is a GATK tool designed to detect somatic short variants, mainly single-nucleotide variants (SNVs) and small insertions and deletions (indels).

### What problem does Mutect2 solve?

The main problem is finding mutations that are present in a tumor but are not simply inherited genetic variants.

Cancer samples can be complicated because a tumor can contain both cancer cells and normal cells. Mutect2 is designed specifically for somatic variant calling and helps identify possible tumor-specific mutations.

### What is its input?

A typical tumor-normal analysis can use:

- Tumor BAM file
- Matched normal BAM file
- Reference genome
- Germline resource
- Panel of normals
- Other supporting resources depending on the workflow

Mutect2 can also be used in tumor-only mode.

### What does it produce?

Mutect2 produces a VCF containing candidate somatic variants. It also produces statistics that can be used during the later filtering stage.

The output normally goes through another GATK tool called `FilterMutectCalls`.

### Where does it fit into the cancer variant-calling workflow?

**BAM → Mutect2 → Raw VCF → FilterMutectCalls → Filtered VCF**

So Mutect2 is the main variant-calling step in this part of the workflow.

### Strengths

- Designed specifically for somatic variant calling
- Supports tumor-normal analysis
- Can also be used in tumor-only analysis
- Detects SNVs and small indels
- Widely used in cancer genomics
- Has detailed official documentation

### Limitations / difficulties

- The complete workflow has several steps
- Raw calls need further filtering
- It can require significant computing resources
- Reference and supporting resources have to be prepared correctly
- The GATK workflow can be difficult for beginners to understand

### Source

- GATK — Mutect2 official documentation
- GATK — FilterMutectCalls documentation

---

## Project 2 — nf-core/sarek

### Project name

**nf-core/sarek**

### GitHub link

https://github.com/nf-core/sarek

### Purpose

Sarek is a workflow for detecting germline and somatic variants from whole-genome, whole-exome, or targeted sequencing data.

It is designed to automate many steps that would otherwise have to be run manually.

### Input

The pipeline can work with sequencing data such as FASTQ files. It can also start from processed BAM/CRAM files for some stages of the workflow.

For tumor-normal analysis, it can work with paired tumor and normal samples.

### Main workflow

A simplified version of the workflow is:

**FASTQ → Quality Control → Alignment → BAM Processing → Variant Calling → Filtering → Annotation → QC**

### Tools used

Some of the tools supported by Sarek include:

- BWA for alignment
- GATK for variant processing
- Mutect2 for somatic variant calling
- Samtools
- VEP for annotation
- SnpEff for annotation
- MultiQC for quality-control reporting
- Nextflow for workflow management

### Output

Depending on the options used, the pipeline can produce:

- Processed BAM files
- VCF files
- Annotated variants
- Quality-control results
- Reports

### Strengths

- Covers many stages of the sequencing workflow
- Supports germline and somatic analysis
- Supports tumor-normal samples
- Includes several variant callers
- Can perform variant annotation
- Uses Nextflow for workflow automation
- Uses containers to make the workflow more reproducible

### Limitations

- It can be complicated for beginners
- It uses Nextflow rather than Python as its main workflow engine
- There are many tools and configuration options to understand
- Running large sequencing workflows can require significant computing resources

### Interesting feature

One interesting feature is that Sarek supports several different variant callers instead of depending on only one tool. Mutect2 is one of the supported callers for somatic SNVs and indels.

### What we might improve

For our project, we could build a smaller Python-based pipeline focused only on the steps we actually need.

We could also add a simple reporting system that turns the final variant results into easy-to-read tables, summaries and graphs.

### Source

- nf-core/sarek — GitHub repository
- nf-core/sarek — Official documentation

---

# 3. Python's Role

## Python Automation

Python can be used to connect the different tools in our pipeline.

We do not need to rewrite tools such as BWA or GATK in Python. Instead, Python can run these programs in the correct order and check whether each step completed successfully.

Python's `subprocess` module can be used to start external programs.

For example:

    import subprocess

    subprocess.run(
        ["bwa", "mem", "reference.fa", "sample_R1.fastq", "sample_R2.fastq"],
        check=True
    )

The basic idea is:

**Python → BWA → BAM → Mutect2 → VCF**

Python would act as the layer coordinating the different programs.

### Source

- Python Documentation — `subprocess`

---

## Python Data Processing

Once we have a VCF or a variant table, Python can help us process the results.

One useful library is **pandas**, which is designed for working with tabular data.

We could use pandas to:

- Filter variants
- Sort results
- Group variants by gene
- Count variants
- Calculate statistics
- Create summary tables
- Export results to CSV or Excel

For example, a final table could contain:

**Gene | Chromosome | Position | REF | ALT | Quality | Effect**

### Source

- pandas Documentation — DataFrame

---

## Python Reporting

Python can also help turn the results into something easier to understand.

We could generate:

- Tables
- Variant summaries
- Quality statistics
- Graphs
- HTML reports
- Markdown reports

For graphs, libraries such as Matplotlib can be used.

For example, we could create graphs showing:

- Number of variants per chromosome
- SNVs versus indels
- Variants per gene
- Passing versus filtered variants

### Source

- Matplotlib Documentation

---

## AI / ML Possibility

### Could AI be added later?

Yes, but I think this should be a later stage of the project.

Once we have clean and annotated variant data, a small machine-learning model could potentially help prioritize or summarize variants.

It could use information such as:

- Gene
- Allele frequency
- Variant type
- Predicted impact
- Quality information
- Other annotation features

The AI would not replace the actual variant caller. It would be an additional layer that could help organize or prioritize the results.

---

# 4. Overall Understanding

After researching sequencing formats, Mutect2, an existing pipeline and Python's role, the basic idea of our project is:

**FASTQ → Alignment → BAM → Mutect2 → VCF → Filtering → Annotation → Python Processing → Report**

### What each part does

**FASTQ**

Raw sequencing reads.

↓

**Alignment**

Finds where the reads belong in the reference genome.

↓

**BAM**

Stores the aligned reads.

↓

**Mutect2**

Looks for possible somatic mutations.

↓

**VCF**

Stores the variants that were called.

↓

**Filtering and Annotation**

Removes or marks unreliable calls and adds information about the variants.

↓

**Python**

Automates the workflow, processes the results and creates readable reports.

### Main idea

We are not trying to replace existing bioinformatics tools.

The main idea is to build a **Python layer around these tools** so the workflow is easier to run, understand and report.

---

# 5. Research Summary

### What I studied

- DNA sequencing
- FASTQ
- BAM
- VCF
- Alignment
- GATK
- Mutect2
- FilterMutectCalls
- nf-core/sarek
- Python subprocess
- pandas
- Python reporting
- Possible AI/ML applications

### Main thing I learned

A cancer variant-calling pipeline is not one single program. It is a series of connected steps, where each tool has a specific job.

The basic idea is:

**Raw sequencing data → Alignment → Variant Calling → Filtering → Annotation → Reporting**

Python can connect these steps together and make the workflow easier to automate and understand.

---

# Sources

- EMBL-EBI — High-throughput sequencing and cancer genomics
- Galaxy Training Network — FASTQ format
- SAMtools / GA4GH — SAM, BAM and VCF specifications
- NCI Genomic Data Commons — VCF documentation
- GATK — Mutect2 official documentation
- GATK — FilterMutectCalls documentation
- nf-core/sarek — GitHub repository
- nf-core/sarek — Official documentation
- Python Documentation — subprocess
- pandas Documentation — DataFrame
- Matplotlib Documentation