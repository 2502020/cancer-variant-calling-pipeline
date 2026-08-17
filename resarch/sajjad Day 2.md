# 1. FastQC - Quality Control

## What is FastQC?

FastQC is a quality-control tool used to check the quality of
high-throughput sequencing data.

It helps identify possible problems in sequencing data before
downstream analysis.

## Why is FastQC important?

Quality checking is an important early step in a sequencing pipeline.
Poor-quality sequencing data can affect later analysis, including
variant calling.

FastQC provides quality-control information that can help us inspect
the quality of the input data.

## Input

FastQC commonly works with sequencing data such as:

- FASTQ files
- BAM files
- SAM files

For our project, FASTQ is the most relevant format if we decide to
start the pipeline from raw sequencing reads.

## Output

FastQC generates quality-control results, including an HTML report
and supporting output files.

The report can contain information about aspects such as:

- Per-base sequence quality
- Sequence quality scores
- GC content
- Sequence length
- Adapter-related information
- Overrepresented sequences

## Basic Workflow

FASTQ
↓
FastQC
↓
Quality Control Report
↓
Continue to downstream analysis

## Possible Role in Our Project

FastQC could be the first stage of our pipeline if we decide to accept
raw FASTQ files as input.

Our Python program could potentially run FastQC and then organize its
output for the user.

Possible architecture:

Python
↓
Run FastQC
↓
Generate QC Report
↓
Check/Display Results
↓
Continue Pipeline

## Python Integration

FastQC is an external bioinformatics program. We do not need to
reimplement FastQC in Python.

Instead, Python could potentially execute the FastQC command using the
Python `subprocess` module.

Conceptually:

Python Program
↓
subprocess
↓
FastQC
↓
HTML/QC Results
↓
Python Pipeline

We will test this approach during the coding phase.

## Advantages

- Provides an early quality check.
- Produces an understandable report.
- Can help identify problems before downstream analysis.
- Can be incorporated into an automated workflow.

## Limitations

FastQC is a quality-control tool, not a variant caller or variant
annotation tool.

It does not identify cancer-causing variants by itself.

## Relevance to Our Project

FastQC could provide the quality-control stage of our pipeline.

The possible workflow would be:

FASTQ
↓
FastQC
↓
Quality Control
↓
Alignment
↓
Variant Calling
↓
VCF
↓
Annotation

Whether FastQC will be included in the final prototype will depend on
our final input format and technical feasibility.

## Source

- Babraham Bioinformatics - FastQC
  https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

- FastQC Documentation
  https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/# 2. BWA/BWA-MEM2 - Sequence Alignment

## What is sequence alignment?

Sequence alignment is the process of mapping sequencing reads to a
reference genome.

The purpose is to determine where each sequencing read is most likely
located in the reference genome.

This is an important step because variant calling needs aligned
sequencing data to identify possible differences between the sample and
the reference genome.

## What is BWA?

BWA (Burrows-Wheeler Aligner) is a software package used for mapping
sequencing reads to a reference genome.

It is commonly used in next-generation sequencing analysis.

## What is BWA-MEM?

BWA-MEM is an algorithm within the BWA software designed for mapping
sequencing reads to a reference genome.

It is commonly used for relatively long sequencing reads.

## What is BWA-MEM2?

BWA-MEM2 is an implementation of the BWA-MEM algorithm designed to
provide improved computational performance while maintaining the
overall BWA-MEM approach.

It can be considered as a possible alignment tool for our pipeline.

## Why is alignment important?

Raw sequencing reads do not directly tell us their exact position in the
genome.

Alignment maps the reads against a reference genome so that downstream
tools can analyze the evidence at specific genomic positions.

## Input

A simplified alignment process can use:

- FASTQ sequencing reads
- Reference genome

For paired-end sequencing, two FASTQ files may represent the two reads
of each pair.

## Output

The alignment process can produce a SAM file, which can then be converted
to BAM or CRAM for more efficient storage and processing.

Simplified flow:

FASTQ
↓
BWA/BWA-MEM2
↓
SAM/BAM/CRAM

## Basic Workflow

A simplified cancer genomics workflow can be:

FASTQ
↓
Quality Control
↓
BWA/BWA-MEM2
↓
Aligned Reads
↓
BAM/CRAM
↓
Variant Calling

## Possible Role in Our Project

If we decide that our pipeline will start from raw FASTQ sequencing
data, BWA-MEM2 could potentially be used as the alignment stage.

Our Python program could potentially run the alignment software and
organize its output.

Possible architecture:

Python
↓
Run BWA/BWA-MEM2
↓
Generate Alignment Output
↓
BAM/CRAM
↓
Variant Calling

## Python Integration

BWA/BWA-MEM2 is an external bioinformatics program.

We do not need to implement the alignment algorithm ourselves.

Python could potentially execute the external command using the
`subprocess` module.

Conceptually:

Python Program
↓
subprocess
↓
BWA/BWA-MEM2
↓
SAM/BAM/CRAM
↓
Python Pipeline

The exact implementation will be tested during the coding phase.

## Advantages

- Widely used approach for sequence alignment.
- Can map sequencing reads to a reference genome.
- Produces data that can be used by downstream variant-calling tools.
- Can potentially be controlled from a Python pipeline.

## Limitations

- Alignment can require significant computational resources for large
  sequencing datasets.
- It requires a suitable reference genome.
- The software and reference genome need to be correctly configured.
- Large real-world cancer sequencing datasets may take considerable
  time and storage.

## Relevance to Our Project

Alignment could be an important stage if we want to demonstrate a
pipeline starting from raw sequencing reads.

The possible workflow is:

FASTQ
↓
FastQC
↓
BWA/BWA-MEM2
↓
BAM/CRAM
↓
Mutect2
↓
VCF
↓
VEP
↓
Annotated Variants

However, we still need to determine whether running the complete
FASTQ-to-VCF workflow is practical within our three-week project.

## Important Decision

We should not automatically include alignment in the final project
without testing its computational requirements.

If full FASTQ processing is too demanding, we could use an already
aligned dataset or begin from a suitable VCF dataset for part of the
prototype.

This decision will be made after further research and feasibility
testing.

## Sources

- BWA GitHub:
  https://github.com/lh3/bwa

- BWA-MEM2 GitHub:
  https://github.com/bwa-mem2/bwa-mem2

- BWA-MEM2 Documentation:
  https://github.com/bwa-mem2/bwa-mem2 # 3. Mutect2 - Somatic Variant Calling

## What is Mutect2?

Mutect2 is a tool from the Genome Analysis Toolkit (GATK) designed for
somatic short-variant discovery.

It is used to identify possible somatic single-nucleotide variants (SNVs)
and small insertions and deletions (indels) in sequencing data.

## Why is Mutect2 relevant to our project?

Our project focuses on cancer variant analysis.

Cancer cells can acquire genetic changes that are not inherited through
the germline. These are called somatic variants.

Mutect2 is therefore a possible tool for the variant-calling stage of our
cancer genomics pipeline.

## What is the input?

Mutect2 can work with aligned sequencing data such as BAM or CRAM files
together with a reference genome.

Cancer analysis may also use a matched normal sample, depending on the
analysis design.

A simplified input is:

- Tumor sequencing data
- Normal sequencing data, when available
- Reference genome

## What is the output?

A major output of Mutect2 is a VCF file containing candidate somatic
variants.

Simplified flow:

BAM/CRAM
↓
Mutect2
↓
Candidate Somatic Variants
↓
VCF

## What types of variants can it identify?

Mutect2 is designed for somatic short variants, including:

- Single-nucleotide variants (SNVs)
- Small insertions
- Small deletions (indels)

## Basic Workflow

A simplified workflow is:

Tumor/Normal BAM or CRAM
↓
Mutect2
↓
Candidate Variants
↓
VCF
↓
Filtering
↓
Annotation

The complete GATK somatic variant workflow can contain additional steps.

## Possible Role in Our Project

Mutect2 could be used as the variant-calling engine while our Python
program acts as the main controller.

Our Python application would not attempt to recreate the Mutect2
variant-calling algorithm.

Instead, Python could potentially:

- Check input files
- Run Mutect2
- Organize output files
- Read the resulting VCF
- Pass variants to later processing and annotation stages

## Python Integration

Mutect2 is an external command-line bioinformatics tool.

Python could potentially run it using the `subprocess` module.

Conceptually:

Python
↓
subprocess
↓
Mutect2
↓
VCF
↓
Python Processing

## Advantages

- Specifically designed for somatic short-variant discovery.
- Suitable for cancer-related variant analysis.
- Can be incorporated into a larger bioinformatics workflow.
- Produces variant information that can be stored in VCF format.

## Limitations

- Mutect2 is a sophisticated tool and requires appropriate input data
  and configuration.
- A complete somatic variant-calling workflow involves more than simply
  running one command.
- Large sequencing datasets can require considerable computational
  resources.
- Correct interpretation requires appropriate biological and technical
  context.

## Relevance to Our Project

Mutect2 is a strong candidate for the variant-calling stage if we decide
to build a pipeline starting from aligned sequencing data.

Possible workflow:

FASTQ
↓
FastQC
↓
BWA/BWA-MEM2
↓
BAM/CRAM
↓
Mutect2
↓
VCF
↓
VEP
↓
Filtering / Analysis
↓
Report

## Important Decision

We will not finalize Mutect2 as the variant caller until we have tested
the required environment, dataset and computational requirements.

## Source

- GATK - Mutect2 Documentation:
  https://gatk.broadinstitute.org/hc/en-us/articles/9570422171291-Mutect2

- GATK Documentation:
  https://gatk.broadinstitute.org/# 4. VEP - Variant Effect Predictor

## What is VEP?

VEP stands for Variant Effect Predictor.

It is a tool developed by Ensembl for predicting the effects of genetic
variants on genes, transcripts and other genomic features.

## Why is VEP relevant to our project?

Variant calling tells us that possible variants have been identified.

However, a list of variants alone does not provide all the biological
information needed to understand them.

Variant annotation can add information about where a variant occurs and
its possible effect.

VEP is therefore a possible annotation tool for our pipeline.

## What is the input?

VEP can take variant information as input, including variants represented
in formats such as VCF.

A simplified workflow is:

VCF
↓
VEP
↓
Annotated Variant Results

## What is the output?

VEP can provide information about the predicted consequences of variants,
including information related to genes, transcripts and other genomic
features.

The exact information depends on the selected options and annotation
resources.

## What information can VEP provide?

Depending on the configuration, VEP can provide information such as:

- Gene affected by a variant
- Transcript information
- Variant consequence
- Genomic location
- Predicted effects
- Existing annotation information
- Additional variant-related information

## Basic Workflow

A simplified annotation workflow is:

VCF
↓
VEP
↓
Annotated Variants
↓
Filtering
↓
Analysis
↓
Report

## Difference Between Variant Calling and Annotation

Variant calling and annotation are different stages.

### Variant Calling

The goal is to identify possible genetic variants from sequencing data.

### Variant Annotation

The goal is to add useful biological and genomic information to those
identified variants.

Simplified:

Sequencing Data
↓
Variant Calling
↓
VCF
↓
VEP
↓
Annotated Results

## Possible Role in Our Project

VEP could be used after variant calling.

Our Python application could potentially:

- Provide the VCF as input
- Run VEP
- Collect the annotation output
- Process the annotated variants
- Filter and prioritize results
- Generate a final report

## Python Integration

VEP is an external tool.

Python could potentially execute it using the `subprocess` module.

Conceptually:

Python
↓
subprocess
↓
VEP
↓
Annotated Output
↓
Python
↓
Filtering / Analysis / Report

## Advantages

- Provides biological and genomic annotation.
- Can identify genes and transcripts affected by variants.
- Can provide predicted variant consequences.
- Can be incorporated into an automated pipeline.

## Limitations

- Annotation depends on the selected databases and resources.
- Correct interpretation of annotations requires biological knowledge.
- VEP configuration can become complex.
- Large variant datasets may require significant processing time.

## Relevance to Our Project

Annotation is an important stage because our project should provide more
than a simple list of detected variants.

A possible pipeline is:

Variant Calling
↓
VCF
↓
VEP
↓
Annotated Variants
↓
Python Filtering
↓
Prioritized Results
↓
Report

## Important Decision

VEP is currently a candidate annotation tool.

We will compare it with other possible annotation approaches before
making the final implementation decision.

## Sources

- Ensembl - Variant Effect Predictor:
  https://www.ensembl.org/info/docs/tools/vep/index.html

- Ensembl VEP Documentation:
  https://www.ensembl.org/info/docs/tools/vep/index.html# 5. pysam - BAM/CRAM Processing

## What is pysam?

pysam is a Python library that provides access to genomic data formats
commonly used in sequencing analysis.

It provides Python interfaces for working with formats such as:

- SAM
- BAM
- CRAM
- VCF/BCF through related functionality

## Why is pysam relevant to our project?

Our possible pipeline may produce aligned sequencing data in BAM or CRAM
format after the alignment stage.

If our Python application needs to inspect or process aligned sequencing
data, pysam could provide a Python-based way to access that information.

## What are BAM and CRAM?

BAM is a binary version of the SAM alignment format.

CRAM is another compressed format used for storing sequencing alignment
data.

These formats are commonly used for storing aligned sequencing reads.

## Possible Input

pysam can work with genomic files such as:

- SAM
- BAM
- CRAM

## Possible Uses

pysam could potentially be used to:

- Open alignment files
- Read sequencing alignments
- Access reads
- Inspect genomic regions
- Extract alignment information
- Process genomic data from Python

## Basic Workflow

A possible use in our project is:

BAM/CRAM
↓
pysam
↓
Python
↓
Extract / Analyze Data
↓
Results

## Possible Role in Our Project

pysam could be useful if our Python application needs direct access to
aligned sequencing data.

For example:

Python
↓
pysam
↓
Read BAM/CRAM
↓
Extract Information
↓
Analyze Results

However, we should only include pysam if our final project actually
requires direct BAM/CRAM processing.

## Python Integration

Unlike FastQC, BWA and Mutect2, pysam is a Python library.

Therefore, it can be imported directly into Python code.

Conceptually:

```python
import pysam# 6. cyvcf2 - VCF/BCF Processing

## What is cyvcf2?

cyvcf2 is a Python library designed for reading and processing VCF and
BCF files.

VCF is an important format in our project because variant-calling tools
can produce variant results in VCF format.

## Why is cyvcf2 relevant to our project?

After variant calling, our pipeline may need to read the resulting VCF
file and process the variants.

cyvcf2 could allow our Python application to access individual variant
records and their information.

## Input

cyvcf2 can work with:

- VCF files
- BCF files

## Possible Uses

cyvcf2 could be used to:

- Read VCF files
- Access variant records
- Extract variant information
- Process variant fields
- Filter variants
- Prepare variant information for further analysis

## Basic Workflow

VCF
↓
cyvcf2
↓
Python
↓
Variant Processing
↓
Filtering / Analysis
↓
Report

## Possible Role in Our Project

If our pipeline produces a VCF file after variant calling, cyvcf2 could
be used by our Python application to read and process the variants.

Possible architecture:

Variant Caller
↓
VCF
↓
cyvcf2
↓
Python
↓
Filtering
↓
Prioritization
↓
Report

## Python Integration

cyvcf2 can be imported directly into Python.

A simple example is:

```python
from cyvcf2 import VCF

vcf = VCF("variants.vcf")

for variant in vcf:
    print(variant.CHROM, variant.POS, variant.REF, variant.ALT)# 7. pandas - Data Analysis and Processing

## What is pandas?

pandas is a Python library used for data manipulation and analysis. It
provides useful data structures such as DataFrames for working with
tabular data.

## Why is pandas relevant to our project?

After variant calling and annotation, our project may contain many
variant records and annotation fields.

pandas could help us organize this information into tables and perform
operations such as filtering, sorting and summarization.

## Possible Uses

pandas could be used for:

- Organizing variant information
- Filtering variants
- Sorting variants
- Selecting important columns
- Grouping results
- Calculating summaries
- Preparing tables
- Preparing data for reports
- Supporting visualization

## Basic Workflow

Annotated Variant Data
↓
Python
↓
pandas DataFrame
↓
Filtering
↓
Sorting
↓
Analysis
↓
Report

## Possible Role in Our Project

pandas could be part of the downstream Python analysis layer.

For example:

VCF
↓
cyvcf2
↓
Python
↓
pandas
↓
Filter / Sort / Analyze
↓
Final Results

## Python Integration

pandas can be imported directly into Python.

A simple example is:

```python
import pandas as pd

data = {
    "Gene": ["TP53", "EGFR", "BRCA1"],
    "Position": [7579472, 55249071, 43071077],
    "Effect": ["missense", "missense", "frameshift"]
}

df = pd.DataFrame(data)

print(df)
---

### 8. Python `subprocess` — Running External Bioinformatics Tools

```markdown
# 8. Python subprocess - Running External Bioinformatics Tools

## What is subprocess?

subprocess is a Python module that allows a Python program to create and
communicate with external processes.

## Why is subprocess relevant to our project?

Our project is written in Python, but several bioinformatics tools we
are researching are separate command-line programs.

Examples include:

- FastQC
- BWA/BWA-MEM2
- Mutect2
- VEP

Instead of trying to rewrite these complex bioinformatics tools in
Python, our Python application could potentially run them as external
programs.

## Basic Concept

Python Application
↓
subprocess
↓
External Bioinformatics Tool
↓
Output File
↓
Python Processing

## Possible Role in Our Project

Python could act as the main controller of the pipeline.

For example:

Python
↓
Run FastQC
↓
Check result
↓
Run BWA/BWA-MEM2
↓
Check result
↓
Run Mutect2
↓
Check result
↓
Run VEP
↓
Process Results

This would allow our Python project to connect multiple established
bioinformatics tools into one workflow.

## Basic Python Example

```python
import subprocess

result = subprocess.run(
    ["some_command"],
    capture_output=True,
    text=True
)

print(result.stdout)# 9. Complete Technical Workflow

## What is a technical workflow?

A technical workflow describes how the different stages of our cancer
variant analysis pipeline connect with each other.

Each stage receives data from the previous stage and produces data that
can be used by the next stage.

## Possible Complete Workflow

Based on the research completed so far, a possible workflow is:

Raw Sequencing Data
↓
FASTQ
↓
FastQC
↓
Quality Control
↓
BWA/BWA-MEM2
↓
BAM/CRAM
↓
Mutect2
↓
VCF
↓
VEP
↓
Annotated Variants
↓
Python Processing
↓
Filtering / Prioritization
↓
Analysis
↓
Report

## Stage 1 - Raw Sequencing Data

The pipeline could begin with sequencing data stored in FASTQ files.

FASTQ contains sequencing reads and their associated quality information.

## Stage 2 - Quality Control

FastQC could be used to examine the quality of the sequencing data.

FASTQ
↓
FastQC
↓
Quality Control Report

## Stage 3 - Alignment

BWA/BWA-MEM2 could be used to align sequencing reads to a reference
genome.

FASTQ
↓
BWA/BWA-MEM2
↓
SAM/BAM/CRAM

## Stage 4 - Variant Calling

Mutect2 could potentially be used to identify candidate somatic
short variants.

BAM/CRAM
↓
Mutect2
↓
VCF

## Stage 5 - Variant Annotation

VEP could potentially add biological and genomic information to the
identified variants.

VCF
↓
VEP
↓
Annotated Variants

## Stage 6 - Python Processing

Our Python application could process the resulting variant information.

Possible Python technologies include:

- cyvcf2 for VCF processing
- pandas for tabular data analysis
- pysam if BAM/CRAM processing is required
- subprocess for running external bioinformatics tools

## Stage 7 - Filtering and Analysis

The Python layer could filter and organize variants according to
criteria selected for the project.

Possible operations include:

- Selecting variants based on available annotation
- Sorting variants
- Removing unwanted records
- Creating summary tables
- Preparing data for visualization

The exact filtering criteria will be decided after we study the dataset
and annotation output.

## Stage 8 - Report

The final stage could present processed results in a clear format.

Possible outputs include:

- Summary tables
- Variant statistics
- Charts
- Annotated variant information
- A final report

## Overall Architecture

```text
                  Python Application
                         |
                         ↓
                      FASTQ
                         |
                         ↓
                       FastQC
                         |
                         ↓
                    BWA/BWA-MEM2
                         |
                         ↓
                      BAM/CRAM
                         |
                         ↓
                      Mutect2
                         |
                         ↓
                        VCF
                         |
                         ↓
                        VEP
                         |
                         ↓
                 Annotated Variants
                         |
                         ↓
              cyvcf2 / pandas / pysam
                         |
                         ↓
               Filtering / Analysis
                         |
                         ↓
                     Final Report # 11. Input and Output Options

## Why are input and output important?

Before developing the pipeline, we need to decide what type of data the
user will provide and what results our system will produce.

The choice of input format affects the complexity of the entire project.

## Possible Input Formats

### FASTQ

FASTQ contains raw sequencing reads and their quality information.

Possible workflow:

FASTQ
↓
FastQC
↓
Alignment
↓
Variant Calling
↓
VCF

Using FASTQ would allow us to demonstrate more stages of a complete
sequencing pipeline.

However, processing raw sequencing data can require significant
computational resources and storage.

### BAM/CRAM

BAM and CRAM contain aligned sequencing reads.

If we start from BAM/CRAM, we could skip the initial alignment stage.

Possible workflow:

BAM/CRAM
↓
Variant Calling
↓
VCF
↓
Annotation
↓
Analysis

This could reduce the complexity of our prototype.

### VCF

VCF contains genetic variant information.

Starting with VCF would allow us to focus mainly on:

- Variant processing
- Annotation
- Filtering
- Prioritization
- Analysis
- Visualization
- Reporting

Possible workflow:

VCF
↓
Python
↓
Annotation
↓
Filtering
↓
Analysis
↓
Report

## Comparison

| Input | Advantages | Challenges |
|---|---|---|
| FASTQ | Demonstrates a larger pipeline | High computational requirements |
| BAM/CRAM | Skips alignment | Still requires genomic processing |
| VCF | Easier for a prototype | Does not demonstrate raw sequencing processing |

## Possible Output Formats

Our project could produce several types of output.

### VCF

A VCF file could contain variant-calling or processed variant results.

### Annotated Variant Table

The Python application could convert relevant variant information into a
readable table.

Possible columns include:

- Chromosome
- Position
- Reference allele
- Alternate allele
- Gene
- Consequence
- Quality
- Other selected annotation fields

### Summary Statistics

The application could calculate statistics such as:

- Total variants
- Variants by chromosome
- Variants by consequence
- Variants passing selected filters

### Visualization

The project could generate charts to make the results easier to
understand.

### Final Report

The final system could produce a report containing:

- Input information
- Quality information
- Number of variants
- Filtered variants
- Important annotations
- Summary tables
- Visualizations

## Recommended Prototype Direction

At this stage, we should investigate both a full FASTQ-based workflow and
a smaller VCF-based workflow.

Because our project has a limited development period, starting from an
appropriate demonstration dataset may be more practical.

The final input format should be selected after feasibility testing.

## Possible Final Output

A possible final result could be:

Input
↓
Python Pipeline
↓
Processed Variants
↓
Filtering
↓
Annotation
↓
Summary Table
↓
Charts
↓
Final Report

## Current Decision

No final input format has been selected yet.

We will make the decision after testing available datasets, tools,
computational requirements and the time available for implementation.# 12. Technical Feasibility

## What is technical feasibility?

Technical feasibility means determining whether the proposed project can
actually be developed and demonstrated using the available time,
software, hardware, data and technical knowledge.

## Main Challenge

A complete cancer variant-calling pipeline can involve many specialized
tools and large sequencing datasets.

Our project has a limited development period, so implementing every stage
of a production-level bioinformatics pipeline may not be realistic.

## Main Components We Need

A possible complete pipeline requires:

- Python
- FASTQ/BAM/CRAM/VCF data
- Reference genome
- FastQC
- BWA/BWA-MEM2
- Mutect2
- VEP
- Python libraries
- Appropriate computing resources

## Computational Requirements

Some stages can require significant computational resources.

For example:

- Alignment can require substantial CPU and memory.
- Variant calling can be computationally intensive.
- Large sequencing datasets require considerable storage.
- Annotation may require additional databases and resources.

Therefore, we should test the tools with small datasets before attempting
large real-world datasets.

## Software Dependencies

Our project may depend on several external programs.

Each dependency must be:

- Installed correctly
- Configured correctly
- Tested
- Compatible with our development environment

Python libraries will also need to be documented in a requirements file.

## Data Availability

We need a dataset that is:

- Suitable for testing
- Small enough to process within our available resources
- Legally and practically usable
- Appropriate for demonstrating the pipeline

Public datasets may be considered after checking their access,
licensing and technical requirements.

## Possible Development Approaches

### Approach 1 - Full Pipeline

FASTQ
↓
FastQC
↓
BWA/BWA-MEM2
↓
Mutect2
↓
VEP
↓
Filtering
↓
Report

### Advantages

- Demonstrates a larger portion of the bioinformatics workflow.
- More closely resembles a complete variant-analysis pipeline.

### Challenges

- More dependencies.
- More computational requirements.
- More difficult to debug.
- More difficult to complete within a short development period.

---

### Approach 2 - Simplified Pipeline

BAM/CRAM
↓
Variant Calling
↓
VCF
↓
Annotation
↓
Python Processing
↓
Report

This removes the raw-read quality-control and alignment stages.

---

### Approach 3 - Focused Python Prototype

VCF
↓
Python
↓
Variant Processing
↓
Filtering
↓
Prioritization
↓
Visualization
↓
Report

### Advantages

- Easier to develop.
- Allows more focus on our own Python contribution.
- Lower computational requirements.
- Easier to demonstrate with a small dataset.

### Limitation

It would not demonstrate the complete raw-sequencing-to-variant workflow.

## Current Feasibility Assessment

Based on the research so far, a complete production-level cancer
variant pipeline is too large to recreate within our limited project
period.

However, a focused Python-based prototype that uses established
bioinformatics tools and concentrates on automation, processing,
filtering, visualization and reporting appears more realistic.

## Proposed Strategy

We should first test the most important tools with small datasets.

The testing should determine:

1. Which input format is practical.
2. Which external tools can run successfully.
3. How much computational resources are required.
4. Which Python libraries are actually necessary.
5. Which stages we can realistically implement.
6. Which feature can become our main project contribution.

## Important Principle

We should not implement tools such as FastQC, BWA, Mutect2 or VEP from
scratch.

Instead, our Python application can control established tools where
appropriate and focus our development effort on the parts that we can
meaningfully implement ourselves.

## Final Feasibility Decision

The final architecture should be selected only after practical testing.

Our goal should be a working, understandable and demonstrable prototype
rather than an unnecessarily large pipeline that cannot be completed or
tested properly. 
