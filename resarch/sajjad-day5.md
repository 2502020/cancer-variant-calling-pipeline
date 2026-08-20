# Sajjad - Day 5 Research

## 1. Project Environment Setup

### What is the project environment?

The project environment is the setup required to develop and run our
Python-based cancer variant analysis pipeline.

A consistent environment is important because our project may depend on
specific Python libraries and external bioinformatics tools.

### What do we need?

The basic development environment can include:

- Python
- A virtual environment
- Git
- GitHub
- Required Python libraries
- Required bioinformatics tools
- A suitable test dataset

### Virtual Environment

A Python virtual environment keeps the project's Python packages
separate from other projects.

It can be created using:## 2. Installing and Managing Python Dependencies

### What are dependencies?

Dependencies are external Python packages that our application needs to
perform specific tasks.

Possible libraries for our project include:

- pandas
- cyvcf2
- pysam
- Biopython
- matplotlib

The final list will depend on which features are actually implemented.

### Installing Packages

Packages can be installed using `pip`.

For example:

```bash
pip install pandas cyvcf2 pysam biopython matplotlib## 3. FastQC Implementation

### What is FastQC?

FastQC is a quality-control tool used to check the quality of sequencing
data.

It can produce reports that help identify potential problems in FASTQ
sequencing files.

### Why do we need FastQC?

Quality control is an important early stage of the pipeline.

Before continuing to later stages, we should examine whether the input
sequencing data has acceptable quality.

The basic workflow is:

```text
FASTQ
  ↓
FastQC
  ↓
Quality Control Report
  ↓
Continue Pipeline## 4. Quality Control Results

### What are quality control results?

Quality control results are the information produced after running FastQC
on sequencing data.

These results help us understand whether the input FASTQ data has
potential quality problems before continuing to later stages.

### What should we examine?

Important FastQC results can include:

- Per-base sequence quality.
- Sequence length.
- GC content.
- Adapter-related information.
- Sequence duplication.
- Overrepresented sequences.

### Why are these results important?

If the sequencing data has quality problems, those problems may affect
later analysis.

Therefore, the quality-control stage should be checked before continuing
with alignment and variant calling.

### FastQC Report

FastQC commonly produces an HTML report that can be opened in a web
browser.

It also produces a data file containing information about the quality
checks.

Example output:

```text
results/
└── fastqc/
    ├── sample_fastqc.html
    └── sample_fastqc.zip## 5. Sequence Alignment Implementation

### What is sequence alignment?

Sequence alignment is the process of matching sequencing reads to a
reference genome.

The purpose is to determine where each sequencing read belongs in the
reference genome.

### Why is alignment important?

Variant calling needs aligned sequencing data.

The basic workflow is:

```text
FASTQ
  ↓
Quality Control
  ↓
Sequence Alignment
  ↓
BAM/CRAM
  ↓
Variant Calling## 6. SAM/BAM File Processing

### What are SAM and BAM files?

SAM (Sequence Alignment/Map) is a text-based format used to store
information about aligned sequencing reads.

BAM is the binary, compressed version of SAM and is commonly used for
efficient storage and processing of alignment data.

### Why are BAM files important?

After sequence alignment, the reads need to be stored in a format that
can be efficiently processed by downstream tools.

The basic workflow is:

```text
FASTQ
  ↓
Alignment
  ↓
SAM
  ↓
BAM
  ↓
Variant Calling## 7. Somatic Variant Calling with Mutect2

### What is somatic variant calling?

Somatic variant calling is the process of identifying genetic changes
that may have been acquired by tumor cells during a person's lifetime.

In cancer analysis, the goal is to identify variants that are present in
the tumor but are absent or present at a different level in the matched
normal sample.

### Why is Mutect2 useful?

Mutect2 is a GATK tool designed for detecting somatic short variants,
including:

- Single-nucleotide variants (SNVs)
- Small insertions and deletions (indels)

It can analyze tumor and matched-normal sequencing data.

### Basic Input

A typical Mutect2 analysis requires information such as:

- Tumor BAM/CRAM file.
- Matched normal BAM/CRAM file, when available.
- Reference genome.
- Reference indexes and other required resources.

A simplified workflow is:

```text
Tumor BAM/CRAM
       +
Normal BAM/CRAM
       +
Reference Genome
       ↓
     Mutect2
       ↓
Candidate VCF
       ↓
Filtering
       ↓
Final Somatic Variants## 8. VCF Validation

### What is VCF validation?

VCF validation means checking whether the Variant Call Format (VCF) file
produced by the variant-calling stage is valid and suitable for the next
stages of the pipeline.

### Why is VCF validation important?

Our pipeline depends on the VCF output from variant calling.

If the VCF is missing, incorrectly formatted or contains unexpected
information, later stages such as annotation and filtering may fail.

Therefore, the pipeline should check the VCF before continuing.

### What can we check?

Basic validation can include:

- Does the VCF file exist?
- Can the VCF file be opened?
- Does it contain the expected VCF header?
- Are chromosome and position fields available?
- Are reference and alternate alleles present?
- Is the file compressed or indexed when required?
- Does the file contain variant records?

### Basic Python Check

Python can first check whether the expected VCF file exists:

```python
from pathlib import Path

vcf_file = Path("results/somatic.vcf.gz")

if vcf_file.exists():
    print("VCF file found.")
else:
    print("Error: VCF file was not found.")## 9. Variant Annotation with VEP

### What is variant annotation?

Variant annotation means adding useful biological information to the
variants identified during variant calling.

Variant calling tells us that a possible variant was detected, while
annotation helps us understand where the variant occurs and what its
possible effect may be.

### What is VEP?

VEP (Variant Effect Predictor) is an Ensembl tool used to annotate
genetic variants.

It can provide information about:

- Affected genes.
- Transcripts.
- Variant consequences.
- Predicted effects on genes or proteins.
- Other available annotation information.

### Why do we need VEP?

A VCF file mainly contains information about the detected variants.

For our project, we want to provide more useful information about those
variants.

The simplified workflow is:

```text
Variant Calling
      ↓
VCF
      ↓
VEP Annotation
      ↓
Annotated Variants
      ↓
Filtering / Analysis
      ↓
Report## 10. Variant Filtering and Prioritization

### What is variant filtering?

Variant filtering means removing variants that do not meet the selected
quality or project criteria.

Variant calling can produce many candidate variants. Filtering helps
reduce this list to variants that are more suitable for further analysis.

### Why is filtering important?

Without filtering, the output may contain a large number of candidate
variants that are difficult to analyze.

Filtering can help:

- Remove low-quality candidate variants.
- Reduce the number of variants for analysis.
- Focus on variants meeting defined criteria.
- Prepare results for annotation and reporting.

### What is variant prioritization?

Prioritization means ranking or selecting variants that may be more
relevant for further investigation.

Prioritization can use information such as:

- Variant quality.
- Variant consequence.
- Gene information.
- Allele frequency, when available.
- Other annotation information.

### Simplified Workflow

```text
Annotated VCF
      ↓
Quality Filtering
      ↓
Annotation-based Filtering
      ↓
Prioritization
      ↓
Selected Variants
      ↓
Analysis / Report## 11. Pipeline Testing with a Small Dataset

### Why do we need testing?

Testing is important to make sure that our pipeline works correctly
before using it for larger datasets.

Because cancer sequencing files can be very large, testing the complete
workflow on a small suitable dataset can make development easier and
faster.

### What should we test?

We should test each stage separately before testing the complete
pipeline.

The main stages are:

```text
Input
  ↓
Quality Control
  ↓
Alignment
  ↓
BAM Processing
  ↓
Variant Calling
  ↓
VCF Validation
  ↓
Annotation
  ↓
Filtering
  ↓
Analysis
  ↓
Report## 13. Testing and Evaluation Metrics

### Why do we need evaluation?

After implementing the pipeline, we need to determine whether it works
correctly and produces useful results.

Testing helps us identify errors in individual stages and in the complete
workflow.

### What should we evaluate?

We can evaluate different parts of the pipeline, including:

- Whether each stage completes successfully.
- Whether expected output files are produced.
- Whether the VCF can be read correctly.
- Whether annotation is completed.
- Whether filtering works according to the defined rules.
- Whether the final report is generated correctly.

### Possible Metrics

Useful measurements can include:

- Number of input reads.
- Number of variants detected.
- Number of variants remaining after filtering.
- Number of annotated variants.
- Number of successfully completed pipeline stages.
- Runtime for each stage, where practical.
- Number of pipeline errors.

### Example Evaluation

A simple evaluation table could be:

| Stage | Expected Result | Actual Result | Status |
|---|---|---|---|
| FastQC | QC report created | To be tested | Pending |
| Alignment | BAM created | To be tested | Pending |
| Variant Calling | VCF created | To be tested | Pending |
| Annotation | Annotated results | To be tested | Pending |
| Filtering | Filtered variants | To be tested | Pending |
| Reporting | Final report | To be tested | Pending |

The actual results should be filled in after running the pipeline.

### Correctness

The pipeline should be checked to make sure that files are passed
correctly from one stage to the next.

For example:

```text
FASTQ
  ↓
BAM
  ↓
VCF
  ↓
Annotated VCF
  ↓
Filtered Results
  ↓
Report

```bash
python -m venv venv
