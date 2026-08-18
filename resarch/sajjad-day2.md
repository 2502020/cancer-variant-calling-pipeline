# Sajjad - Day 3 Research

## 1. Project Architecture

### What is project architecture?

Project architecture means deciding how our Python project will be
organized and how its different parts will work together.

Our project will contain different parts instead of putting everything
inside one Python file.

### Why do we need project architecture?

A clear structure will make our project:

- Easier to understand
- Easier to develop
- Easier to test
- Easier to fix when something goes wrong
- Easier for both team members to work on

### Proposed Project Structure

```text
cancer-variant-pipeline/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
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
│
└── results/## 2. Python Libraries and Their Roles

### Why do we need Python libraries?

Python libraries provide ready-made functions that can save development
time.

Instead of creating everything from the beginning, we can use suitable
libraries to read, process and analyze genomic data.

### 1. pandas

pandas is a Python library used for working with tables and structured
data.

### Possible use in our project

We could use pandas to:

- Organize variant information into tables.
- Filter variants.
- Sort variant results.
- Calculate simple statistics.
- Prepare data for reports.

Example:

```text
VCF Data
   ↓
Python / pandas
   ↓
Table of Variants
   ↓
Filtering and Analysis## 3. Pipeline Workflow Design

### What is a pipeline workflow?

A pipeline workflow is the order in which the different steps of our
project will be performed.

Each step takes some input, processes it, and produces an output that can
be used by the next step.

### Proposed Workflow

Our initial cancer variant analysis workflow is:

Input Data
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
Filtering
↓
Analysis
↓
Report

### 1. Input Data

The pipeline will first receive sequencing or genomic data.

The exact input format will be selected after testing suitable datasets.

Possible formats include:

- FASTQ
- BAM/CRAM
- VCF

### 2. Quality Control

If our pipeline starts with raw sequencing data, a quality-control tool
such as FastQC can be used.

The purpose is to check whether the sequencing data has quality problems
before continuing.

### 3. Alignment

If raw sequencing reads are being used, an alignment tool such as
BWA/BWA-MEM2 can be used to align the reads to a reference genome.

The result can be an aligned sequencing file such as BAM.

### 4. Variant Calling

A variant-calling tool such as Mutect2 can be used to identify possible
somatic variants from suitable cancer sequencing data.

The results can be stored in VCF format.

### 5. VCF Processing

The VCF contains information about the detected variants.

Python can be used to read and process the VCF.

### 6. Variant Annotation

An annotation tool such as VEP can add information about genes,
transcripts and possible variant consequences.

### 7. Filtering

Python can apply selected filters to the annotated variants.

For example, we may filter results based on available quality,
annotation or other selected fields.

The exact filtering rules will be decided during development and
testing.

### 8. Analysis

The Python program can calculate useful statistics and organize the
selected variants.

Possible results include:

- Number of variants
- Variants by chromosome
- Variants by consequence
- Filtered variant list

### 9. Report

The final stage can produce an understandable report containing tables,
statistics and, if implemented, charts.

### Role of Python

Python can control the overall workflow and process the results.

For example:

Python
↓
Run external tool
↓
Check output
↓
Process output
↓
Run next step
↓
Generate report

### Important Point

Not every stage has to be implemented from scratch in Python.

Established bioinformatics tools can perform specialized tasks, while
our Python application can connect the stages and process the results.

### Initial Workflow Diagram

Input
↓
FastQC
↓
BWA/BWA-MEM2
↓
Mutect2
↓
VCF
↓
VEP
↓
Python Filtering
↓
Python Analysis
↓
Report

### Conclusion

The workflow provides a basic structure for our project.

The final workflow may be simplified depending on the dataset,
computational requirements and available development time.## 4. Python Module and File Design

### Why do we need separate Python files?

Our project should not contain all of the code in one large Python file.

Separate modules allow each part of the project to have a clear
responsibility.

This makes the project easier to understand, test and maintain.

### Proposed File Structure

```text
cancer-variant-pipeline/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
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
│
└── results/## 5. Possible Unique Feature

### What is a unique feature?

A unique feature is a useful function that makes our project different
from a basic pipeline that only runs existing bioinformatics tools.

Our project should focus on a feature that is useful, realistic and
possible to complete within our available development time.

### Possible Unique Features

#### 1. Beginner-Friendly Interface

Our Python program could provide a simple interface that guides the user
through the pipeline.

Instead of requiring the user to remember many commands, the program
could provide clear options and instructions.

Example:

```text
Cancer Variant Pipeline

1. Select Input Data
2. Run Quality Check
3. Run Variant Analysis
4. Annotate Variants
5. Filter Results
6. Generate Report
```markdown
## 6. Initial Technical Design

### What is the initial technical design?

The initial technical design describes how the different parts of our
Python application could work together.

The design may change after we test the tools and datasets.

### Overall System

The basic system can be represented as:

```text
                User
                 ↓
          Python Application
                 ↓
            Input Data
                 ↓
        Pipeline Controller
                 ↓
      ┌──────────┼──────────┐
      ↓          ↓          ↓
   FastQC       BWA       Mutect2
                              ↓
                             VCF
                              ↓
                             VEP
                              ↓
                      Python Processing
                              ↓
                    Filtering / Analysis
                              ↓
                     Results / Report## 7. Testing and Validation

### What is testing?

Testing means checking whether our Python pipeline works correctly.

We should test each part of the project before testing the complete
pipeline.

### Why is testing important?

Our project uses multiple steps and tools. A problem in one step could
affect the later steps.

Testing helps us:

- Find errors
- Check that inputs are accepted correctly
- Check that outputs are created correctly
- Make sure the different stages work together
- Improve the reliability of the project

### 1. Input Testing

First, we should check whether the input file is valid and available.

The program should check:

- Does the input file exist?
- Is the file in the expected format?
- Can the file be opened and read?

If the input is incorrect, the program should show a clear error
message.

### 2. Individual Tool Testing

Each external tool should be tested separately before connecting it to
the complete pipeline.

For example:

```text
Test FastQC
     ↓
Check Report
     ↓
Test Alignment
     ↓
Check BAM
     ↓
Test Variant Calling
     ↓
Check VCF## 8. Project Limitations and Risks

### What are project limitations?

Project limitations are things that may make the project difficult or
prevent us from implementing every planned feature.

Since our project has limited development time and resources, we need to
identify these problems early.

### 1. Large Dataset Size

Cancer sequencing datasets can be very large.

Large files may require:

- More storage
- More RAM
- More processing time

Therefore, we should start development and testing with a small suitable
dataset.

### 2. Computational Requirements

Some bioinformatics tools can require significant CPU and memory.

For example, alignment and variant calling may take considerable time
when working with large datasets.

We need to test the tools on the available computer before deciding on
the final workflow.

### 3. Multiple Software Dependencies

Our pipeline may depend on several external tools.

For example:

- FastQC
- BWA/BWA-MEM2
- Mutect2
- VEP

Installing and configuring all of these tools correctly may be
challenging.

### 4. Tool Compatibility

Different tools may require specific versions, file formats or
configuration settings.

If one tool produces an output that another tool cannot use correctly,
the pipeline may fail.

We therefore need to test the connection between each stage.

### 5. Limited Development Time

Our project has a limited development period.

Trying to implement a complete professional-level cancer analysis system
may make the project too large.

We should therefore focus on a smaller and realistic prototype.

### 6. Dataset Availability

We need an appropriate dataset for testing.

The dataset should be:

- Accessible
- Suitable for our project
- Small enough for testing
- Appropriate for the selected workflow

We also need to consider any access or usage restrictions.

### 7. Scientific Complexity

Cancer genomics is a complex scientific field.

Our project should not claim that it can diagnose cancer or replace
professional medical analysis.

The system should be presented as a research/educational prototype for
processing and analyzing genomic variant data.

### 8. Accuracy of Results

Our Python program may depend on external tools and the quality of the
input data.

Incorrect input, poor-quality sequencing data or incorrect configuration
can affect the results.

Therefore, results should be checked and validated where possible.

### 9. AI Feature Complexity

If an AI-assisted feature is included, it may increase the complexity of
the project.

We should only add an AI feature if:

- It has a clear purpose.
- Suitable data is available.
- It can be implemented within the project time.
- Its results can be evaluated.

Otherwise, the project should focus on reliable pipeline automation,
filtering, analysis and reporting.

### Risk Management

To reduce these risks, we can:

1. Start with a small dataset.
2. Test each tool separately.
3. Build the pipeline step by step.
4. Use version-controlled Python code.
5. Keep the project architecture simple.
6. Test every major output.
7. Avoid unnecessary features.
8. Keep backup plans if a tool cannot run successfully.

### Conclusion

The biggest risks are dataset size, computational requirements, software
dependencies, scientific complexity and limited development time.

A focused and modular Python prototype will make the project more
realistic and easier to complete successfully.## 9. Final Project Goal

### What are we trying to build?

Our goal is to build a focused Python-based cancer variant analysis
pipeline.

The system should help process genomic data, identify or work with
genetic variants, add useful information, filter the results and present
them in an understandable way.

### Basic Idea

The overall idea is:

Input Data
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
Filtering
↓
Analysis
↓
Report

### What will Python do?

Python will act as the main controller and processing layer.

It can:

- Take input from the user.
- Check whether the input is valid.
- Run selected external bioinformatics tools.
- Manage the different pipeline stages.
- Read and process variant data.
- Filter variants.
- Calculate useful statistics.
- Generate tables and reports.

### What will external tools do?

Specialized bioinformatics tools can perform complex tasks.

Possible tools include:

- FastQC for quality checking.
- BWA/BWA-MEM2 for alignment.
- Mutect2 for somatic variant calling.
- VEP for variant annotation.

We should use established tools instead of trying to recreate their
complex algorithms ourselves.

### What should the user receive?

The final system should provide understandable results rather than only
raw technical files.

Possible outputs include:

- Variant results.
- Filtered variant tables.
- Summary statistics.
- Simple visualizations.
- A final report.

### What should make our project useful?

Our project should focus on making the workflow easier to use and
understand.

Possible useful features include:

- Automatic processing.
- Variant filtering.
- Result summaries.
- Simple charts.
- Automatic report generation.
- A beginner-friendly interface.

The final unique feature will be selected after testing and feasibility
checking.

### What are we NOT trying to build?

We are not trying to recreate large professional platforms such as
Sarek or Galaxy.

We are also not trying to build our own versions of complex tools such
as Mutect2 or VEP.

Our goal is a smaller and realistic Python prototype that connects
appropriate tools and adds useful processing and reporting features.

### Final Development Goal

The final project should be:

- Python-based.
- Modular.
- Easy to understand.
- Testable.
- Able to process an appropriate genomic dataset.
- Capable of producing useful variant results.
- Realistic to complete within the available development time.

### Important Note

The exact input format, external tools, libraries and final features are
not completely fixed yet.

They will be selected after testing the available datasets, tools and
technical requirements.

### Conclusion

The main goal is to create a practical Python-based cancer variant
analysis pipeline that connects existing bioinformatics tools with our
own Python processing, filtering, analysis and reporting.

The project should focus on a realistic working prototype rather than
trying to reproduce a complete professional cancer genomics platform.## 10. Day 3 Research Conclusion

Today we focused on how our Python cancer variant analysis project will
be designed and organized.

We planned a modular project structure so that different parts of the
pipeline can be kept in separate Python files.

We also studied the possible roles of Python libraries such as pandas,
cyvcf2, pysam and Biopython. We learned that the `subprocess` module can
allow Python to run external bioinformatics tools.

We designed an initial pipeline:

Input Data
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
↓
Filtering
↓
Analysis
↓
Report

We also discussed possible project features such as automatic result
summaries, variant filtering, simple visualizations and report
generation.

Testing and validation were identified as important parts of the
project. We should test individual tools and Python modules before
testing the complete pipeline.

We also identified important limitations, including large datasets,
computational requirements, software dependencies, dataset availability
and limited development time.

Our main conclusion is that the project should remain focused and
realistic. Python should control and process the pipeline while
established bioinformatics tools perform complex specialized tasks.

The exact tools, input format and final features will be selected after
practical testing.## 11. Sources

1. Python Documentation — subprocess
   https://docs.python.org/3/library/subprocess.html

2. pandas Documentation
   https://pandas.pydata.org/docs/

3. pysam Documentation
   https://pysam.readthedocs.io/

4. cyvcf2 Documentation
   https://brentp.github.io/cyvcf2/

5. Biopython Documentation
   https://biopython.org/docs/

6. FastQC
   https://www.bioinformatics.babraham.ac.uk/projects/fastqc/

7. GATK — Mutect2 Documentation
   https://gatk.broadinstitute.org/hc/en-us/articles/9570422171291-Mutect2

8. Ensembl — Variant Effect Predictor (VEP)
   https://www.ensembl.org/info/docs/tools/vep/index.html

9. nf-core/Sarek
   https://github.com/nf-core/sarek

10. Galaxy Project
    https://galaxyproject.org/## 12. Day 3 Final Checklist

### Research Completed

- [x] Project architecture researched.
- [x] Python libraries and their possible roles researched.
- [x] Pipeline workflow designed.
- [x] Python modules and file structure planned.
- [x] Possible unique features identified.
- [x] Initial technical design prepared.
- [x] Testing and validation approach planned.
- [x] Project limitations and risks identified.
- [x] Final project goal defined.
- [x] Day 3 research conclusion written.
- [x] Sources documented.

### Main Day 3 Result

By the end of Day 3, we have a basic technical plan for our Python
cancer variant analysis project.

We now have an initial idea of:

- How the project will be organized.
- Which Python libraries may be useful.
- How the pipeline will work.
- What each Python module may do.
- Which features could be added.
- How we will test the project.
- What limitations we need to consider.

The design is still flexible and can be changed after we test the actual
datasets and tools.

### Next Step

The next stage is to review the research from Day 1, Day 2 and Day 3,
finalize the practical project design, and then begin setting up the
Python project for implementation.
