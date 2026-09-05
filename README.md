# Cancer Variant Calling and Annotation Pipeline

A Python-based bioinformatics pipeline that processes cancer sequencing data through quality control, alignment, variant calling, filtering, annotation, and reporting - orchestrated entirely by Python using industry-standard tools.

## Overview

This pipeline does not reimplement bioinformatics algorithms. Instead, Python acts as an orchestrator, calling established tools (FastQC, BWA, samtools, bcftools) via subprocess, managing the flow of data between stages, handling errors, and logging progress.

## Pipeline Stages

FASTQ -> Quality Control (FastQC) -> Alignment (BWA) -> BAM Processing (samtools) -> Variant Calling (bcftools) -> Filtering (custom Python) -> Annotation (custom Python) -> Final Report (custom Python)

## Project Structure

cancer-variant-calling-pipeline/
- data/input/ - FASTQ sequencing files
- data/reference/ - Reference genome
- results/fastqc/, alignment/, variants/, annotation/, filtering/, report/
- logs/ - Pipeline execution logs
- src/cancer_pipeline/ - config.py, validator.py, logger.py, pipeline.py, qc.py, alignment.py, bam_processing.py, variant_calling.py, filtering.py, annotation.py, reporting.py
- config.json
- main.py
- requirements.txt
- README.md

## How to Run

1. Set up a Python virtual environment and activate it:
   python3 -m venv .venv
   source .venv/bin/activate

2. Install required system tools:
   sudo apt install -y fastqc bwa samtools bcftools

3. Configure config.json with your input/reference paths and desired quality threshold.

4. Run the full pipeline:
   python main.py

5. Check results in results/report/final_report.txt and pipeline logs in logs/pipeline.log

## Notes

- This implementation uses small, synthetic test data to validate the full pipeline architecture end-to-end.
- Variant calling uses bcftools as a lightweight, real alternative to GATK Mutect2.
- Annotation is a simplified stand-in for VEP, tagging each variant with its type, position, and base change.
- The pipeline is designed so each stage can be swapped for a more heavyweight/production tool without changing the overall orchestration logic in pipeline.py.
