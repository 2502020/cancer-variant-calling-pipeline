# Sajjad - Day 4 Research

## 1. Python Environment Setup

### What is a Python environment?

A Python environment is a setup where we can install and run the
libraries required by our project.

For our project, using a separate virtual environment can help keep the
project's Python packages separate from other Python projects.

### Why do we need it?

Our project may use libraries such as:

- pandas
- cyvcf2
- pysam
- Biopython

A virtual environment helps us manage these dependencies without
affecting other Python projects.

### Basic setup

A virtual environment can be created using:## 2. GitHub Project Structure

### Why do we need a project structure?

Our project contains multiple stages and different types of code.
Keeping everything in one file would make the project difficult to
understand and maintain.

We therefore plan to organize the project into separate folders and
modules.

### Proposed Structure

```text
cancer-variant-pipeline/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pipeline/
│   ├── quality_control.py
│   ├── alignment.py
│   ├── variant_calling.py
│   └── annotation.py
│
├── processing/
│   ├── vcf_processing.py
│   ├── filtering.py
│   └── analysis.py
│
├── reporting/
│   └── report.py
│
├── data/
└── results/## 3. Input Validation

### What is input validation?

Input validation means checking whether the data provided to the
pipeline is suitable before processing begins.

### Why is it important?

If the user provides a missing, incorrect or unsupported file, the
pipeline should detect the problem early instead of failing later.

### What should we check?

The program should check:

- Whether the input file exists.
- Whether the provided path is actually a file.
- Whether the file format is supported.
- Whether the file can be read.
- Whether required input information is available.

### Possible Input Formats

Depending on the final pipeline, possible input formats include:

- FASTQ
- BAM
- CRAM
- VCF

The final supported formats will be decided after testing the selected
workflow.

### Example Validation Logic

```text
User provides input
        ↓
Does the file exist?
        ↓
      Yes
        ↓
Is the format supported?
        ↓
      Yes
        ↓
Can the file be read?
        ↓
      Yes
        ↓
Continue pipeline## 4. Running External Bioinformatics Tools from Python

### Why do we need external tools?

Cancer genomic analysis involves complex tasks such as quality control,
sequence alignment, variant calling and variant annotation.

Instead of recreating these complex algorithms ourselves, our Python
application can control established bioinformatics tools.

### Python subprocess

Python provides the `subprocess` module for starting and communicating
with external programs.

A simplified example is:

```python
import subprocess

result = subprocess.run(
    ["fastqc", "data/sample.fastq"],
    capture_output=True,
    text=True
)

print(result.stdout)## 5. Pipeline Automation

### What is pipeline automation?

Pipeline automation means allowing the Python program to run the
different stages of the workflow in the correct order with less manual
work from the user.

### Why is automation important?

Our project contains several stages. Without automation, the user may
need to run every tool separately.

With automation, Python can control the process:

```text
Input
  ↓
Quality Control
  ↓
Alignment
  ↓
Variant Calling
  ↓
Annotation
  ↓
Filtering
  ↓
Analysis
  ↓
Report## 6. VCF Processing in Python

### What is VCF processing?

VCF processing means reading and working with the variant information
stored in a VCF (Variant Call Format) file.

After variant calling, our pipeline can produce a VCF file containing
information about detected variants.

Python can then process this information for filtering, analysis and
reporting.

### Why is VCF processing important?

The VCF file contains the results that we need to work with in the later
stages of our project.

Our Python application may need to:

- Read variants from the VCF.
- Extract important fields.
- Count variants.
- Filter variants.
- Analyze variant information.
- Prepare data for reporting.

### Important VCF Information

A VCF record can contain information such as:

- Chromosome
- Position
- Reference allele
- Alternate allele
- Quality
- Filter status
- INFO fields
- Sample information

For example:

```text
CHROM    POS    REF    ALT    QUAL    FILTER
chr1     12345  A      G      99      PASS## 7. Variant Filtering

### What is variant filtering?

Variant filtering means removing variants that do not meet selected
criteria so that the final results contain variants that are more useful
for further analysis.

Variant calling can produce many candidate variants. Not every detected
variant will be equally useful, so filtering is an important step.

### Why is filtering important?

Filtering can help:

- Remove low-quality variants.
- Reduce the number of variants that need to be examined.
- Focus on variants that meet selected criteria.
- Prepare cleaner results for analysis and reporting.

### What information can be used?

Depending on the VCF and the selected variant-calling workflow, possible
filtering criteria may include:

- Quality score.
- Filter status.
- Read depth.
- Allele information.
- Variant allele frequency (VAF), when available.
- Annotation information.

The exact filtering criteria will be selected after we examine the
actual VCF produced by our pipeline.

### Basic Filtering Example

A simple Python example using `cyvcf2` could be:

```python
from cyvcf2 import VCF

vcf = VCF("results/variants.vcf")

for variant in vcf:
    if variant.QUAL is not None and variant.QUAL >= 30:
        print(
            variant.CHROM,
            variant.POS,
            variant.REF,
            variant.ALT,
            variant.QUAL
        )## 8. Variant Analysis

### What is variant analysis?

Variant analysis means examining the variants that remain after variant
calling, annotation and filtering.

The purpose is to organize the variant information and identify useful
patterns in the results.

### Why is variant analysis important?

A VCF file can contain many variants. Simply displaying all of them may
not be easy for a user to understand.

Python can help organize the information and produce useful summaries.

### What can we analyze?

Depending on the information available in the VCF and annotation results,
we could analyze:

- Total number of variants.
- Number of variants per chromosome.
- Number of SNVs and indels.
- Number of variants passing filters.
- Variant quality statistics.
- Variant consequences after annotation.
- Other useful fields available in the results.

### Using pandas

The `pandas` library can be used to organize variant information into
tables.

For example:

```python
import pandas as pd

data = {
    "Chromosome": ["chr1", "chr1", "chr2", "chr2"],
    "Position": [1000, 2500, 3000, 4500],
    "Reference": ["A", "C", "G", "T"],
    "Alternate": ["G", "T", "A", "C"]
}

df = pd.DataFrame(data)

print(df)## 9. Result Visualization

### What is result visualization?

Result visualization means presenting variant analysis results using
simple charts and graphs.

Instead of showing only large tables of numbers, charts can make the
results easier to understand.

### Why is visualization useful?

Visualization can help users quickly understand:

- How many variants were detected.
- Where variants are located.
- How variants are distributed across chromosomes.
- How many variants remain after filtering.
- What types of variant consequences are present.

### Possible Visualizations

#### 1. Variants by Chromosome

A bar chart can show the number of variants found on each chromosome.

Example:

```text
Chromosome
chr1  █████████████
chr2  █████████
chr3  ██████
chr4  ████## 10. Automatic Report Generation

### What is automatic report generation?

Automatic report generation means allowing the Python program to create
a summary of the pipeline results without requiring the user to manually
prepare the report.

### Why is it useful?

Our pipeline may produce a large amount of variant information.

A report can organize the important results into an easier-to-understand
format.

The report could include:

- Total number of variants.
- Number of variants before filtering.
- Number of variants after filtering.
- Variants by chromosome.
- Variant consequence information.
- Selected variant details.
- Tables.
- Simple charts.
- Pipeline status and summary.

### Basic Report Workflow

```text
Pipeline Results
      ↓
Python Analysis
      ↓
Calculate Statistics
      ↓
Create Tables / Charts
      ↓
Generate Report
      ↓
Final Results## 11. Error Handling and Logging

### What is error handling?

Error handling means detecting problems during the pipeline and
responding to them in a clear and controlled way.

Our project uses multiple stages and external tools, so errors can occur
at different points.

### Why is error handling important?

Without proper error handling, the program may stop unexpectedly or
continue even though an earlier stage failed.

Our pipeline should:

- Detect errors.
- Show a clear error message.
- Identify which stage failed.
- Stop when continuing would produce incorrect results.
- Help the developer understand what went wrong.

### Common Errors

Possible errors include:

- Input file does not exist.
- Unsupported file format.
- Required software is not installed.
- External tool fails.
- Output file is missing.
- Invalid VCF data.
- Incorrect file path.
- Insufficient permissions.

### Basic Python Error Handling

Python provides `try` and `except` for handling errors.

Example:

```python
try:
    with open("data/input.vcf", "r") as file:
        data = file.read()

except FileNotFoundError:
    print("Error: Input file was not found.")## 12. Day 4 Implementation Plan

### Purpose

After researching the technical requirements, the next step is to move
from planning toward implementation.

The project should be developed gradually instead of trying to build the
complete pipeline at once.

### Step 1: Create the Python Project

First, create the basic project structure and Python environment.

The project should contain:

- `main.py`
- Required Python modules
- `requirements.txt`
- `README.md`
- `.gitignore`

### Step 2: Implement Input Validation

The program should first check whether the required input exists and can
be processed.

Basic checks should include:

- File existence.
- File type.
- File readability.
- Required input information.

### Step 3: Test External Tools

Before connecting all tools together, each required bioinformatics tool
should be tested separately.

Possible tools include:

- FastQC
- BWA/BWA-MEM2
- Mutect2
- VEP

The final tools will depend on the selected workflow and available
environment.

### Step 4: Create the Pipeline Controller

Python should control the order of the different stages.

The initial structure can be:

```text
Input
 ↓
Quality Control
 ↓
Alignment
 ↓
Variant Calling
 ↓
Annotation
 ↓
Filtering
 ↓
Analysis
 ↓
Report## 13. Day 4 Research Conclusion

Today we focused on how our cancer variant analysis project can move from
research and planning toward practical implementation.

We researched how to set up the Python environment, organize the GitHub
project, validate input files and use Python to control external
bioinformatics tools.

We also studied how the pipeline can be automated so that different
stages run in the correct order.

We investigated how Python can process VCF files, filter variants and
perform basic analysis using suitable Python libraries.

We also planned how the results could be visualized and included in an
automatic report.

Finally, we researched error handling, logging and the implementation
order for developing the project.

The main workflow identified during Day 4 is:

Input
↓
Input Validation
↓
Quality Control
↓
Alignment
↓
Variant Calling
↓
VCF Processing
↓
Annotation
↓
Filtering
↓
Analysis
↓
Visualization
↓
Report

Our main conclusion is that we should build the project gradually.
First, we should create a working minimum prototype and test each
component before adding optional or advanced features.

The next step is to begin practical implementation and test the selected
tools and workflow with a suitable dataset.## 14. Sources

1. Python Documentation — venv
   https://docs.python.org/3/library/venv.html

2. Python Documentation — subprocess
   https://docs.python.org/3/library/subprocess.html

3. Python Documentation — logging
   https://docs.python.org/3/library/logging.html

4. pandas Documentation
   https://pandas.pydata.org/docs/

5. cyvcf2 Documentation
   https://brentp.github.io/cyvcf2/

6. pysam Documentation
   https://pysam.readthedocs.io/

7. Biopython Documentation
   https://biopython.org/docs/

8. FastQC
   https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

9. GATK — Mutect2 Documentation
   https://gatk.broadinstitute.org/hc/en-us/articles/9570422171291-Mutect2

10. Ensembl — Variant Effect Predictor
    https://www.ensembl.org/info/docs/tools/vep/index.html

11. nf-core/Sarek
    https://github.com/nf-core/sarek

12. Galaxy Project
    https://galaxyproject.org/

```bash
python -m venv venv 
