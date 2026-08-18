# Cancer Variant Calling and Annotation Pipeline

## Day 2 Research

**Team Member:** Maham  
**Project Type:** Python / AI  
**Research Phase:** Week 1 - Day 2  
**Date:** 17 August 2026

---

# 1. Existing Cancer Variant Calling and Annotation Projects

For Day 2, I looked at three different existing projects related to cancer variant calling, filtering, annotation and prioritization.

I chose projects that do different things so we can understand what has already been done and where our own project could be different.

The three projects are:

- Strelka2
- SomaticSeq
- CancerVar + OPAI

---

# 2. Project 1 — Strelka2

## Project name

**Strelka2**

## GitHub / official link

https://github.com/Illumina/strelka

## What problem does it solve?

Strelka2 is a small variant caller used to identify germline and somatic variants from sequencing data.

For cancer analysis, it can compare tumor and normal samples and look for somatic SNVs and small indels.

It is designed to be fast while still producing accurate variant calls.

## Input

For somatic analysis, Strelka2 mainly uses:

- Tumor BAM or CRAM
- Normal BAM or CRAM
- Reference genome
- Optional candidate indel VCF from Manta

## Main workflow

A simplified workflow is:

**Tumor/Normal BAM → Candidate detection → Local analysis → Variant scoring → VCF**

Strelka first examines the aligned reads, identifies possible variant locations, analyzes the reads around those locations and then produces the final variant calls.

The workflow can also split the genome into regions so different parts can be processed in parallel.

## Programming language

The main Strelka software is implemented mainly in **C++**, with Python-based workflow/configuration scripts.

## Tools used

Some important tools around the Strelka workflow include:

- Strelka2
- Manta
- Python
- Samtools
- Reference genome
- BAM/CRAM files

For somatic indels, the documentation recommends using Manta to provide additional candidate indels.

## Output

The main output is VCF.

For somatic analysis, Strelka produces separate files for:

- Somatic SNVs
- Somatic indels

It can also produce statistics and a somatic callability track.

## Main features

- Somatic SNV calling
- Somatic indel calling
- Tumor-normal analysis
- Variant filtering/rescoring
- Random-forest based empirical rescoring
- Parallel processing
- WGS, exome and targeted analysis options
- Somatic callability analysis

## Strengths

The main strength I noticed is that Strelka2 focuses on being both fast and accurate.

It also has a useful rescoring step based on a random forest model. This means it is not just making calls and stopping there; it also uses additional features to improve confidence in the calls.

Another useful feature is parallel processing, which is important when working with large sequencing datasets.

## Limitations

One important limitation is that Strelka's somatic workflow requires a matched normal sample.

It can also be complicated for a beginner because the workflow has several configuration and execution steps.

Another thing to note is that the official GitHub repository was archived in April 2026, so it is now read-only.

## What can we learn from it?

We can learn how a real variant caller handles:

- Tumor-normal comparison
- Variant scoring
- Filtering
- Parallel processing
- VCF output

The random-forest rescoring idea is also interesting for our AI/ML part.

## Source

- Illumina Strelka2 GitHub repository
- Strelka2 official User Guide
- Strelka2 research paper, Nature Methods

---

# 3. Project 2 — SomaticSeq

## Project name

**SomaticSeq**

## GitHub / official link

https://github.com/bioinform/somaticseq

## What problem does it solve?

SomaticSeq tries to improve somatic variant detection by combining the results of different variant callers.

Instead of trusting only one caller, it can take results from several callers and use their information together.

It can also use machine learning to distinguish likely true mutations from false positives.

## Input

SomaticSeq can use:

- Tumor BAM
- Normal BAM
- Reference genome
- VCF files from different variant callers
- Optional truth VCF files for training
- Optional databases such as dbSNP or COSMIC

Some supported callers include Mutect2, VarScan2, Strelka2, VarDict, LoFreq and others.

## Main workflow

A simplified version is:

**Multiple Variant Callers → Combine VCFs → Extract Features → Machine Learning / Consensus → Final VCF**

The system can either use a simple consensus approach or use a trained machine-learning model.

## Programming language

SomaticSeq is mainly written in **Python 3**.

It also has R components for AdaBoost, while the newer default XGBoost implementation is written in Python.

## Tools used

Some important tools and libraries are:

- Python
- pandas
- NumPy
- SciPy
- pysam
- XGBoost
- R / AdaBoost
- BEDTools
- Docker
- Mutect2
- Strelka2
- VarDict
- LoFreq

## Output

SomaticSeq can produce:

- VCF files
- TSV files
- Consensus variant calls
- Machine-learning classified variants
- Prediction scores

For example, it can produce classified SNV and indel results.

## Main features

- Combines multiple variant callers
- Extracts sequencing features
- Consensus calling
- Machine-learning classification
- XGBoost support
- AdaBoost support
- SNV and indel processing
- Training using truth sets
- Prediction using trained models
- Parallel processing
- Dockerized workflows

## Strengths

The biggest strength is the use of information from multiple callers.

If one caller makes a questionable call, other callers can provide additional evidence.

The machine-learning component is also very interesting for our project because it shows that ML can be used to help separate likely true variants from false positives.

Another good feature is that SomaticSeq can be used as a Python library instead of only being run as a command-line pipeline.

## Limitations

It can be difficult to set up because it depends on several other variant callers and bioinformatics tools.

Training a useful ML model also requires suitable training or truth data.

The workflow can become computationally heavy when many callers are used.

It is also more focused on improving variant calling rather than providing a simple user-friendly final report.

## What can we learn from it?

SomaticSeq is probably the most useful project for our AI part.

It shows that we do not necessarily need to build a huge deep-learning system.

A smaller machine-learning model can use variant features and existing caller results to produce a useful prioritization or confidence score.

## Source

- SomaticSeq GitHub repository
- SomaticSeq documentation
- Genome Biology paper: "An ensemble approach to accurately detect somatic mutations using SomaticSeq"

---

# 4. Project 3 — CancerVar + OPAI

## Project name

**CancerVar and OPAI**

CancerVar is for cancer variant interpretation, while OPAI stands for **Oncogenic Prioritization by Artificial Intelligence**.

## GitHub / official link

https://github.com/WGLab/CancerVar

Official website:

https://cancervar.wglab.org/

## What problem does it solve?

After variant calling, we can have a large list of variants.

The difficult part is understanding which variants are potentially important.

CancerVar tries to interpret cancer somatic variants using evidence and the AMP/ASCO/CAP guidelines.

OPAI adds a machine-learning component that predicts the oncogenicity of variants.

## Input

CancerVar can take:

- VCF files
- ANNOVAR input
- Annotated variant files
- Variant coordinates
- Gene and nucleotide/protein changes

CancerVar can use ANNOVAR to generate required annotations.

OPAI then uses features from CancerVar and computational prediction scores.

## Main workflow

A simplified workflow is:

**VCF / Variant Data → ANNOVAR Annotation → CancerVar Evidence → Variant Classification → OPAI → Oncogenicity Score**

CancerVar assigns variants to categories such as:

- Tier I — Strong clinical significance
- Tier II — Potential clinical significance
- Tier III — Uncertain significance
- Tier IV — Benign / likely benign

## Programming language

CancerVar and OPAI are mainly **Python-based**.

OPAI uses Python libraries including:

- pandas
- NumPy
- scikit-learn
- PyTorch

## Tools used

Some of the main tools and resources include:

- Python
- ANNOVAR
- pandas
- NumPy
- scikit-learn
- PyTorch
- CancerVar databases
- Clinical evidence
- Computational prediction scores

## Output

CancerVar produces an annotated interpretation containing evidence and a classification.

OPAI produces an oncogenicity prediction score.

CancerVar also has a web interface where users can search variants and view evidence.

## Main features

- Variant annotation
- Evidence-based interpretation
- Cancer-specific classification
- AMP/ASCO/CAP guideline support
- Manual interpretation option
- Web interface
- REST API
- Oncogenicity prediction
- Deep-learning model
- Large precomputed variant database

## Strengths

The biggest strength is that it goes beyond simply calling variants.

It tries to answer the next question:

**"What might this variant mean?"**

Another interesting feature is the combination of rules/evidence with AI.

The project also provides a web interface, which makes the results easier to explore than a command-line-only tool.

## Limitations

CancerVar has a lot of external database and annotation requirements.

The full system is also much bigger than what we could realistically build in three weeks.

The AI component is based on a trained model and a large amount of curated data, so reproducing the whole system would not be realistic for our project.

Also, the tool is intended for non-commercial use according to its repository.

## What can we learn from it?

CancerVar is especially useful for thinking about our project's final stage.

We could take a simpler approach:

**VCF → Annotation → Features → Simple Priority Score → Human-readable Report**

We could focus on explaining why a variant received a certain priority score rather than trying to reproduce CancerVar's complete clinical interpretation system.

## Source

- CancerVar GitHub repository
- CancerVar official website
- Science Advances paper: "CancerVar: An artificial intelligence-empowered platform for clinical interpretation of somatic mutations in cancer"

---

# 5. Comparison Table

| Project | Language | Input | Tools | Output | Strength | Limitation |
|---|---|---|---|---|---|---|
| Strelka2 | C++ + Python | BAM/CRAM | Strelka2, Manta, Python | VCF, statistics | Fast and accurate calling | More complex and requires matched normal for somatic calls |
| SomaticSeq | Python + R | BAM + VCFs from callers | XGBoost, AdaBoost, BEDTools, pysam | VCF + TSV + scores | Combines callers and uses ML | Needs multiple callers/training data |
| CancerVar + OPAI | Python | VCF / annotated variants | ANNOVAR, PyTorch, pandas, scikit-learn | Interpretation + oncogenicity score | Annotation + AI + web interface | Large system and difficult to reproduce fully |

---

# 6. Features Already Available in Existing Projects

While looking at these projects, I noticed that many features we were thinking about already exist somewhere.

| Feature | Strelka2 | SomaticSeq | CancerVar |
|---|---|---|---|
| Variant calling | Yes | Uses other callers | No |
| Variant filtering | Yes | Yes | Yes |
| Variant prioritization | Limited | ML scoring | Yes |
| Annotation | Limited | Limited | Yes |
| Machine learning | Random forest rescoring | XGBoost / AdaBoost | Deep learning |
| Visualization | Limited | Limited | Web interface |
| Automatic reports | Statistics | TSV/VCF outputs | Web results |
| Workflow automation | Yes | Yes | Partial |
| Web interface | No | No | Yes |
| API | No | No | Yes |
| Parallel processing | Yes | Yes | Not the main focus |

## What I noticed

The existing projects are good at individual parts of the problem.

For example:

- Strelka2 is strong at variant calling.
- SomaticSeq is strong at combining callers and ML filtering.
- CancerVar is strong at annotation, interpretation and AI-based prioritization.

But they are generally bigger and more complicated than what we need for a small three-week student project.

---

# 7. Finding the Gap

The main question for us is:

**What can our project do differently instead of simply copying an existing pipeline?**

I think there are a few possible gaps.

## Idea 1 — Simple Python-based end-to-end pipeline

We could make a smaller pipeline that connects the important steps:

**Input → Variant Calling → Filtering → Annotation → Prioritization → Report**

Instead of supporting dozens of tools, we could focus on one clear workflow.

The main advantage would be simplicity.

---

## Idea 2 — Explainable variant prioritization

Instead of only giving a score, our system could explain why a variant was given a higher priority.

For example:

**Priority: High**

Reasons:

- Rare in population database
- High predicted functional impact
- Strong sequencing evidence
- Present in multiple callers
- Cancer-related gene

This would make the AI/ML output easier for a student or researcher to understand.

---

## Idea 3 — Automatic research-style report

Another possible feature is an automatic report generated from the final VCF.

The report could contain:

- Total variants
- Passing variants
- Variant types
- Top genes
- Highest-priority variants
- Simple graphs
- Variant quality information
- ML priority scores

This could be generated automatically using Python.

---

## Idea 4 — Lightweight web dashboard

A simple web interface could allow the user to upload or select a VCF and then see:

- Variant table
- Filters
- Priority scores
- Gene information
- Graphs
- Downloadable report

This would make our project easier to demonstrate.

We do not need to build a large clinical web platform like CancerVar.

---

# 8. AI / ML Possibility

## How is AI already being used?

The projects I looked at show a few different approaches.

SomaticSeq uses machine learning to help distinguish true somatic mutations from false positives.

Strelka2 uses a random forest model for empirical variant rescoring.

CancerVar goes further and uses a deep-learning model to predict oncogenicity.

## Could we build something in three weeks?

I think a **small ML component is realistic**, but a full deep-learning system like CancerVar is not.

We could use a simple model such as:

- Random Forest
- XGBoost
- Logistic Regression

The model could use features such as:

- Variant quality
- Read depth
- Variant allele frequency
- Number of callers supporting the variant
- Population frequency
- Predicted functional impact
- Gene information

The output would be a **priority score**, not a medical diagnosis.

For example:

**Variant A → Priority 0.91**

**Variant B → Priority 0.37**

The system could then rank variants from higher to lower priority.

## Important limitation

This would only be a research/demo feature.

It should not be presented as a system that diagnoses cancer or tells a doctor which treatment to use.

The goal would be to demonstrate how ML can help organize and prioritize variant information.

---

# 9. Public Testing Dataset

## Dataset

**SEQC2 HCC1395 / HCC1395BL**

This is a well-known cancer benchmarking dataset.

HCC1395 is the tumor sample and HCC1395BL is the matched normal sample.

The SEQC2 project was created specifically to provide reference data and high-confidence somatic mutation call sets for benchmarking cancer mutation detection.

## Source

NCBI SRA:

**SRP162370**

The SEQC2 study also provides BAM files, VCF files and a high-confidence somatic mutation call set.

## Formats

The dataset is available in several useful formats:

- FASTQ
- BAM
- VCF

The raw FASTQ data is available through NCBI SRA.

BAM files and VCF call sets are also available through the SEQC2/NCBI resources.

## Size

The complete SEQC2 resource is large.

For example, NVIDIA's official SEQC2 tutorial uses two HCC1395 WGS SRA files and reports that each is about **65 GB**, so the tumor-normal pair is roughly **130 GB** before processing.

This is too large for a simple three-week student project if we try to process everything locally.

## Is it suitable for our project?

**Yes, scientifically it is very suitable.**

The biggest advantage is that it has a high-confidence somatic mutation call set that can be used as a reference when evaluating a variant-calling method.

However, we should probably not start with the complete WGS dataset.

A smaller subset, selected genomic regions, or already processed BAM/VCF data would be more realistic for our project.

## Why I like this dataset

It gives us:

**Tumor + Normal + Sequencing Data + Truth/Reference Variants**

That means we can potentially test whether our pipeline is producing sensible results instead of only showing that the code runs.

### Source

- SEQC2 / Nature Biotechnology
- NCBI SRA — SRP162370
- SEQC2 somatic mutation reference call set
- NVIDIA SEQC2 benchmarking documentation

---

# 10. What Existing Projects Already Do

After comparing the projects, I noticed that existing systems already provide many advanced features:

### Variant calling

Strelka2 and other callers identify possible somatic variants.

### Filtering

Strelka2 and SomaticSeq have ways of filtering or rescoring variants.

### Machine learning

SomaticSeq uses XGBoost/AdaBoost, while CancerVar uses deep learning.

### Annotation

CancerVar uses annotation databases and evidence to interpret variants.

### Prioritization

CancerVar produces oncogenicity scores, while SomaticSeq can produce ML-based classification scores.

### Workflow automation

Strelka2 and SomaticSeq automate multiple analysis steps.

### Web interface

CancerVar provides a web interface for searching and interpreting variants.

### Reports

Several projects produce statistics, tables or other summaries, but the level of user-friendly reporting is different between projects.

---

# 11. Possible Gap for Our Project

I do not think our project should try to compete with these projects in the number of tools or the size of their databases.

Instead, our possible gap could be:

**A small, Python-based, easy-to-understand cancer variant analysis pipeline with explainable prioritization and automatic reporting.**

A possible workflow could be:

**VCF → Filtering → Annotation → Feature Extraction → ML Priority Score → Visualization → Report**

The project would focus more on making the results understandable rather than building another huge variant caller.

---

# 12. What We Could Potentially Build

These are ideas only. We do not need to choose the final feature yet.

### Option 1

**Explainable variant prioritization**

A simple ML model ranks variants and shows the reasons/features behind the score.

### Option 2

**Automatic variant report**

The program takes a VCF and creates an HTML/Markdown report containing tables, graphs and important variants.

### Option 3

**Simple web dashboard**

A user uploads a VCF and can filter variants, view priority scores and generate a report.

### Option 4

**Combination of the above**

A small Python application could combine:

**Filtering + Annotation + ML ranking + Visualization + Report**

This might be more interesting for a BS AI project than just creating another basic variant caller.

---

# 13. Three-Week Reality Check

We only have three weeks, so the project needs to stay realistic.

## Week 1

Focus on understanding and building the basic pipeline.

- Input VCF
- Parse variants
- Basic filtering
- Basic annotation
- Store results in a table

## Week 2

Add the AI/ML component.

- Select useful features
- Prepare training/testing data
- Train a small model
- Generate a variant priority score
- Evaluate the model

## Week 3

Focus on the final user experience.

- Graphs
- Variant table
- Automatic report
- Simple interface if time a