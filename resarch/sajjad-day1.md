 # Cancer Variant Calling and Annotation Pipeline
## Day 1 Research - Sajjad

**Team Members:** Sajjad  
**Project Type:**   Python  
**Research Phase:** Week 1 - Day 1  
**Date:** [16 August 2026]

---

# 1. Cancer Genomics

## What is cancer genomics?

Cancer genomics is the study of genetic information and genetic changes
associated with cancer. By studying these changes, researchers can better
understand how cancer develops and behaves.

## Why is cancer genomics relevant to our project?

Our project focuses on identifying and analyzing genetic variants in
cancer sequencing data. Cancer genomics provides the medical and
biological context for why we need a variant calling and annotation
pipeline.

## Source

- National Cancer Institute — Cancer Genomics Overview
  https://www.cancer.gov/ccg/research/cancer-genomics-overview


# 2. Genome

## What is a genome?

A genome is the complete set of genetic information of an organism.
In humans, the genome is made up of DNA and contains the instructions
that cells use for their functions and development.

## Why is the genome relevant to our project?

Our project analyzes sequencing data to identify genetic differences
or variants. Therefore, understanding the genome and the reference
genome is important for understanding how variants are detected.

## Source

- National Human Genome Research Institute — Genome
  https://www.genome.gov/genetics-glossary/Genome


# 3. Genetic Changes in Cancer

## What are genetic changes in cancer?

Genetic changes are changes in DNA that can occur in cells. Some genetic
changes have little or no effect, while others can affect how cells grow
and divide. Changes that disrupt genes involved in controlling cell
growth and other important cellular processes can contribute to cancer.

## Why are genetic changes important for our project?

Our project aims to identify genetic variants from cancer sequencing
data. After variants are detected, annotation can help us understand
their biological significance and potentially identify variants that
are more relevant to cancer.

## Source

- National Cancer Institute — Genetic Changes and Cancer
  https://www.cancer.gov/about-cancer/causes-prevention/genetics


# 4. Genetic Variants

## What is a genetic variant?

A genetic variant is a difference in the DNA sequence compared with
another or reference sequence. Variants can be harmless, have biological
effects, or in some cases contribute to disease.

## What is an SNV?

An SNV (single-nucleotide variant) is a change involving one nucleotide
or DNA base at a particular position.

## What is an indel?

An indel is an insertion or deletion of one or more bases in a DNA
sequence.

## What is a somatic variant?

A somatic variant is a genetic change that is acquired during a person's
life in cells rather than being inherited through the germline.

## Why are somatic variants important in cancer?

Cancer cells can contain acquired genetic changes that affect their
behavior. Identifying somatic variants can therefore help researchers
study the genetic changes associated with a tumor.

## Sources

- National Human Genome Research Institute — Genetic Variant
  https://www.genome.gov/genetics-glossary/Genetic-Variant

- National Cancer Institute — Genetic Changes and Cancer
  https://www.cancer.gov/about-cancer/causes-prevention/genetics


# 5. Variant Calling

## What is variant calling?

Variant calling is the computational process of identifying possible
genetic differences, called variants, from sequencing data. The process
compares sequencing evidence with a reference genome and identifies
positions where the sample may differ from the reference.

## What is the input?

Variant calling generally uses aligned sequencing data, such as BAM or
CRAM files, together with a reference genome. In cancer analysis, the
workflow may also use information from a matched normal sample or other
resources depending on the variant-calling method.

## What is a reference genome?

A reference genome is a standard DNA sequence used as a baseline for
analyzing and comparing sequencing data. Sequencing reads from a sample
can be aligned to the reference genome so that possible differences
can be identified.

## What types of variants are we interested in?

For our cancer genomics project, we are mainly interested in somatic
short variants such as single-nucleotide variants (SNVs) and small
insertions and deletions (indels).

## What is the output?

A major output of variant calling is a VCF (Variant Call Format) file.
The VCF contains information about detected or candidate variants,
including their genomic positions and reference and alternate alleles,
along with additional information about the variant calls.

## Why is variant calling important in cancer?

Cancer cells can acquire genetic changes that contribute to abnormal
cell behavior. Variant calling helps identify possible somatic genetic
changes in tumor sequencing data. These variants can then be annotated
and analyzed to better understand their possible biological or clinical
significance.

## Example existing tool

Mutect2 is a GATK tool designed for somatic short-variant discovery.
It can be used to identify somatic single-nucleotide variants and small
insertions/deletions from sequencing data.

## Sources

- GATK — Mutect2 Documentation
  https://gatk.broadinstitute.org/hc/en-us/articles/9570422171291-Mutect2

- National Cancer Institute — Cancer Genomics Overview
  https://www.cancer.gov/ccg/research/cancer-genomics-overview


# 6. VCF (Variant Call Format)

## What is a VCF file?

VCF stands for Variant Call Format. It is a standard text-based file
format used to store information about genetic variants identified from
sequencing data.

## Why is VCF important?

VCF is important because it provides a structured way to store the
variants identified during variant calling. It allows the results to be
passed to later stages such as filtering, annotation, analysis, and
reporting.

## What information does a VCF contain?

A VCF can contain information such as:

- Chromosome or contig
- Position of the variant
- Reference allele
- Alternate allele
- Quality information
- Filters applied to the variant
- Additional information about the variant
- Genotype/sample information

## What is the relationship between variant calling and VCF?

Variant calling identifies possible genetic variants from sequencing
data. The identified variants are commonly stored in a VCF file.

The basic flow is:

Sequencing Data → Alignment → Variant Calling → VCF

## Why is VCF important for our project?

VCF will be an important intermediate/output format in our pipeline.
After variants are called, our Python-based system can use the VCF
results for further processing, filtering, annotation, analysis, and
report generation.

## Source

- SAMtools/HTS Specifications — VCF
  https://samtools.github.io/hts-specs/VCFv4.5.pdf


# 7. Variant Annotation

## What is variant annotation?

Variant annotation is the process of adding useful biological and
genomic information to variants identified during variant calling.
Annotation helps us understand where a variant occurs and what its
possible biological effect may be.

## Why do we annotate variants?

Variant calling tells us that a possible genetic variant was detected.
However, the variant itself does not immediately tell us what it means.

Annotation provides additional information that can help researchers
understand and prioritize variants for further investigation.

## What information can annotation provide?

Depending on the annotation tool and databases used, annotation can
provide information such as:

- Gene and transcript affected by the variant
- Genomic location
- Variant consequence
- Predicted effect on a gene or protein
- Population frequency information
- Existing clinical or biological information
- Other databases or predictions related to the variant

## What is VEP?

VEP (Variant Effect Predictor) is a tool developed by Ensembl for
annotating genetic variants. It can determine the genes and transcripts
affected by variants and provide information about their predicted
consequences.

## What is the difference between variant calling and annotation?

Variant calling focuses on identifying possible variants from sequencing
data.

Variant annotation focuses on adding biological and genomic information
to those identified variants.

The simplified workflow is:

Sequencing Data → Variant Calling → VCF → Annotation → Annotated Results

## Why is annotation important for our project?

Annotation is an important stage of our cancer genomics pipeline because
the project should not only identify variants but also provide useful
information about them. Annotated results can then be filtered,
prioritized, analyzed, and presented in a more understandable report.

## Example annotation tool

One possible annotation tool for our project is Ensembl Variant Effect
Predictor (VEP). We will compare VEP with other annotation tools during
our research before deciding which tool is most suitable for our
pipeline.

## Source

- Ensembl — Variant Effect Predictor
  https://www.ensembl.org/info/docs/tools/vep/index.html


# 8. Existing Project 1 - nf-core/Sarek

## What is Sarek?

Sarek is a bioinformatics workflow designed for genomic variant analysis,
including germline and somatic variant analysis. It automates and
organizes multiple stages of the analysis workflow.

## What problem does Sarek solve?

Sarek helps researchers organize and automate multiple steps involved
in genomic analysis instead of running each step manually.

## What is the input?

Sarek can work with different types of sequencing-related input data,
depending on where the user starts the workflow. These can include
sequencing reads and processed files for appropriate workflow stages.

Specific supported inputs and workflow options will be verified from
the official documentation during further research.

## What are the major stages?

The workflow can involve stages such as preprocessing, alignment,
variant calling, filtering and annotation. The exact stages depend on
the selected workflow and parameters.

## What tools does it use?

Sarek integrates multiple established bioinformatics tools for different
stages of the workflow. We will document the important tools and their
roles from the official Sarek documentation.

## What is the output?

The workflow can produce files and results from different analysis
stages, including aligned sequencing data, variant files and annotated
variant results.

## Strengths

- Automates multiple bioinformatics analysis steps.
- Provides a structured and reproducible workflow.
- Supports both germline and somatic variant analysis.
- Integrates established bioinformatics tools.

## Limitations or difficulties observed

One possible difficulty for beginners is the complexity of understanding
and configuring a multi-tool workflow. Sarek uses workflow-management
and bioinformatics technologies that may require additional technical
knowledge.

This is our observation and will be investigated further during the
research phase.

## What can we learn from Sarek?

Sarek shows that a modern variant-analysis pipeline can connect multiple
specialized bioinformatics tools into one workflow. We can study this
approach while designing a simpler Python-based system suitable for our
project and its three-week development period.

## Sources

- nf-core/Sarek GitHub
  https://github.com/nf-core/sarek

- nf-core/Sarek Documentation
  https://nf-co.re/sarek/


# 9. Existing Project 2 - Galaxy

## What is Galaxy?

Galaxy is an open-source platform designed to make data analysis,
including biomedical and bioinformatics analysis, more accessible to
researchers. It provides a web-based environment where users can run
analysis tools and workflows.

## What problem does Galaxy solve?

Bioinformatics analysis can require many different tools and technical
commands. Galaxy provides a graphical and web-based environment that
allows users to organize and run analysis workflows without manually
executing every command.

## What is the input?

Galaxy can work with many types of scientific and genomic data,
depending on the tools and workflows being used. In genomic analysis,
inputs can include sequencing files such as FASTQ and other processed
genomic files.

## What are the major stages?

A Galaxy workflow can connect multiple analysis steps together. A
simplified genomic workflow can include:

Sequencing Data
→ Quality Control
→ Alignment
→ Variant Calling
→ Variant Filtering
→ Annotation
→ Results

The exact stages depend on the workflow selected by the user.

## What tools does Galaxy use?

Galaxy provides access to many bioinformatics tools and allows users to
connect them into workflows. Different tools can be used for quality
control, alignment, variant calling, annotation and other analyses.

## What is the output?

The output depends on the selected workflow. In genomic analysis,
outputs can include processed sequencing data, alignment files, VCF
variant files, annotated results and reports.

## Strengths

- Provides a graphical/web-based interface.
- Makes bioinformatics tools easier to access.
- Allows multiple tools to be connected into workflows.
- Can make complex analysis more accessible to researchers.
- Supports reproducible workflows.

## Limitations or difficulties observed

Galaxy provides a large number of tools and options, which can make the
platform overwhelming for beginners. It is also a general-purpose
platform rather than a small project specifically designed around one
focused cancer variant-analysis pipeline.

## What can we learn from Galaxy?

Galaxy shows the importance of making bioinformatics workflows easier to
use. Our project can take inspiration from this idea by providing a
simple Python-based interface that guides users through the major stages
of cancer variant analysis.

However, our project should remain much smaller and more focused because
we have a limited development period.

## Sources

- Galaxy Project
  https://galaxyproject.org/

- Galaxy Training Network
  https://training.galaxyproject.org/


# 10. Python Technologies

## Biopython

Biopython is a collection of Python tools and libraries for biological
computation. It provides functionality for working with biological
sequences, sequence files and other bioinformatics-related data.

### Possible use in our project

Biopython could be investigated for biological sequence processing and
other basic bioinformatics tasks. We will determine during development
whether it is required for our final pipeline.

### Source

- Biopython Documentation
  https://biopython.org/docs/


## pysam

pysam is a Python library that provides access to files and data formats
commonly used in genomic analysis, including SAM, BAM and CRAM files.

### Possible use in our project

pysam could be useful if our Python pipeline needs to inspect, process or
extract information from aligned sequencing data stored in BAM or CRAM
files.

### Source

- pysam Documentation
  https://pysam.readthedocs.io/


## cyvcf2

cyvcf2 is a Python library designed for reading and processing VCF and
BCF files efficiently.

### Possible use in our project

cyvcf2 could be useful after variant calling because our pipeline will
need to read and process VCF files for filtering, analysis and
potentially reporting.

### Source

- cyvcf2 Documentation
  https://brentp.github.io/cyvcf2/


## pandas

pandas is a Python library for data manipulation and analysis. It
provides data structures such as DataFrames that can be used to organize
and analyze tabular data.

### Possible use in our project

pandas could be useful for organizing variant information into tables,
filtering results, calculating statistics and preparing data for reports.

### Source

- pandas Documentation
  https://pandas.pydata.org/docs/


## Python subprocess

The Python subprocess module allows a Python program to create and
communicate with external processes.

### Possible use in our project

The subprocess module could allow our Python pipeline to run established
bioinformatics command-line tools from within a Python program. This
could help us build a Python-based pipeline without attempting to
reimplement complex variant-calling algorithms ourselves.

### Source

- Python Documentation — subprocess
  https://docs.python.org/3/library/subprocess.html


## Possible role of Python in our project

Python can act as the main controller of our pipeline. Instead of
reimplementing complex scientific algorithms, our application can
organize the workflow, validate inputs, run appropriate tools, process
their outputs, filter variants and generate understandable results.

A possible architecture is:

Input Data
    ↓
Python Pipeline
    ↓
Quality Control
    ↓
Alignment
    ↓
Variant Calling
    ↓
VCF Processing
    ↓
Variant Annotation
    ↓
Filtering and Analysis
    ↓
Report

The exact tools and stages will be selected after further research and
testing.


# 11. Findings From Existing Projects

## Sarek

Sarek demonstrates how multiple specialized bioinformatics tools can be
combined into an automated workflow for germline and somatic variant
analysis.

## Galaxy

Galaxy demonstrates how complex bioinformatics tools can be made more
accessible through a user-friendly interface and workflow system.

## Common idea

Both projects show that cancer genomic analysis involves multiple stages
and specialized tools rather than a single program.

## Opportunity for our project

Our project should not attempt to compete with large platforms such as
Sarek or Galaxy. Instead, we should design a smaller, focused and
educational Python-based cancer variant-analysis pipeline that can be
developed and demonstrated within our available time.

Potential areas for innovation will be investigated during the remaining
research period.


# 12. Initial Pipeline Concept

Based on the research completed on Day 1, our initial concept is a
Python-based cancer variant analysis pipeline.

A simplified workflow is:

Input Sequencing Data
        ↓
Quality Control
        ↓
Alignment
        ↓
Variant Calling
        ↓
VCF
        ↓
Variant Annotation
        ↓
Variant Filtering
        ↓
Variant Analysis
        ↓
Results / Report

Python would act as the main pipeline controller and could communicate
with established bioinformatics tools where appropriate.

The final workflow, tools and unique features will be decided after
further research and feasibility testing.


# 13. Potential Unique Features

During the research phase, we identified several possible directions
that could make our project more useful or interesting.

## 1. Beginner-friendly Python interface

The pipeline could provide a simple interface that guides a user through
the major stages instead of requiring knowledge of many command-line
commands.

## 2. Automated quality and result summary

The system could summarize important statistics from the pipeline and
present them in an understandable format.

## 3. Variant filtering and prioritization

Instead of simply producing a large VCF file, the system could provide
useful filtering and prioritization options to help users focus on
important variants.

## 4. Simple visual reporting

The system could generate charts or tables summarizing detected variants,
their locations, consequences and other available information.

## 5. AI-assisted interpretation

A possible future feature could be an AI-assisted explanation or
prioritization component. This should only be included if it can be
implemented reliably within the project timeline and supported by
appropriate data and scientific sources.

## Important note

These are initial ideas, not final project features. During Week 1 we
will compare existing solutions and determine which feature is realistic,
technically achievable and sufficiently different fr
