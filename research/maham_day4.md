
# Cancer Variant Calling and Annotation Pipeline

## Day 4 Research — Datasets, Reference Genomes, Tools, Annotation, and Data Governance

**Team Member:** Maham
**Project Type:** Python / AI
**Research Phase:** Week 1 - Day 4
**Date:** 19 August 2026

---

# 1. Cancer Genomics Datasets

Cancer genomics datasets are collections of sequencing data (and often clinical information) gathered from tumor and, ideally, matched normal tissue from the same patient. They exist so researchers don't have to sequence their own patients from scratch every time they want to study or test a method.

These datasets generally come in a few different forms:

- **Raw data** — FASTQ or BAM/CRAM files, straight from the sequencer or after alignment.
- **Called variants** — VCF or MAF files, already processed by a variant caller.
- **Clinical/phenotype data** — information about the patient or tumor (cancer type, stage, treatment), usually handled separately from the sequencing data for privacy reasons.
- **Benchmarking/"truth" data** — datasets built specifically so that the correct answer (which mutations are really there) is already known, used to test whether a pipeline is accurate.

For our project we mainly care about the first and last categories: raw or lightly processed sequencing data, ideally with a truth set attached so we can check our own results.

### Source
- NCI Genomic Data Commons — About GDC
- SEQC2 / Nature Biotechnology

---

# 2. Public Cancer Data Sources

The main public sources we identified are:

- **SEQC2 / HCC1395** — a tumor-normal benchmarking pair with a published truth set. Open access.
- **NCI Genomic Data Commons (GDC) / TCGA** — a very large repository covering 33+ cancer types. Some processed summaries are open access; raw reads need controlled access approval.
- **ICGC ARGO** — international cancer genomics data. The old open web portal is retired; most current data needs DACO approval.
- **Genome in a Bottle (GIAB)** — not cancer-specific, but very well-characterized reference samples with truth variant sets. Useful for testing pipeline correctness.
- **1000 Genomes Project** — open, population-scale germline data. Good for practice, not built for tumor-vs-normal comparison.
- **Texas Cancer Research Biobank Open Access pilot** — a smaller, genuinely open-access project that shared tumor/normal genomic data from 7 real cancer cases with essentially no access restrictions (other than not attempting to re-identify participants). Useful to know this kind of fully-open cancer dataset exists, even though it's small.
- **Community-curated subsets** (e.g., bcbio validation workflows on GitHub) — small, pre-trimmed regions of larger datasets, made specifically for testing pipelines without needing huge storage.

### Source
- SEQC2 / Nature Biotechnology
- NCI Genomic Data Commons
- ICGC ARGO — Data Access documentation
- NIST Genome in a Bottle Consortium
- Texas Cancer Research Biobank — Open Access pilot, Scientific Data journal
- bcbio_validation_workflows — GitHub repository

---

# 3. Dataset Requirements

Before picking a dataset, we listed out what we actually need it to have:

- A **tumor sample** and a **matched normal sample** from the same source (needed for somatic variant calling).
- Data in a **standard, well-supported format** (FASTQ, BAM, or VCF).
- A **known truth set**, if possible, so we can measure whether our pipeline's output is actually correct.
- **Open access**, or access that doesn't require a lengthy approval process, since we only have three weeks.
- **Small enough** in size and scope (like a single chromosome or exome region) to realistically download and process on a normal computer.
- Reasonably **well documented**, so we're not guessing about what each file contains.

Datasets that fail more than one or two of these aren't realistic for this project, however scientifically valuable they might be.

---

# 4. FASTQ Data (Quick Recap)

As covered on Day 3: FASTQ is the raw output of a sequencer — millions of short reads, each stored as four lines (identifier, sequence, separator, quality scores). It's the very first input in the pipeline, before any alignment happens.

For this project, we're planning to start from already-aligned BAM files rather than raw FASTQ, mainly to save on processing time and computing resources. FASTQ remains relevant to understand conceptually, since it's where the whole process begins.

### Source
- Galaxy Training Network — FASTQ format

---

# 5. Reference Genome

## What is a reference genome?

A reference genome is a standardized, representative DNA sequence for a species — in our case, human. It's not any one specific person's DNA; it's a composite assembled from many samples, used as the common coordinate system everyone aligns their sequencing reads against.

## Why do we need it?

Every step downstream depends on it:

- **Alignment** needs it to figure out where each read belongs.
- **BAM/CRAM files** store read positions relative to it.
- **VCF files** report variant positions (CHROM, POS) relative to it — so REF and ALT only make sense in the context of the exact reference version used.
- **Annotation tools** (like VEP) need it to know which genes and transcripts sit at which coordinates.

## Which version should we use?

The two commonly used human reference genome builds are **GRCh37 (hg19)** and **GRCh38 (hg38)**. GRCh38 is the more current build and is generally recommended for new work, but a lot of older public datasets (including some SEQC2 files) are distributed against GRCh37. Whichever version we pick, it has to match the version our BAM/VCF files were built against — mixing versions causes incorrect variant positions.

Since we're only working with a subset (one chromosome or a small region), we only need to download that portion of the reference genome, not the full ~3 GB human genome file.

### Source
- Genome Reference Consortium — GRCh37/GRCh38 documentation
- SAMtools / GA4GH — alignment format specifications

---

# 6. BAM/CRAM Files (Quick Recap)

As covered on Day 3: BAM stores aligned sequencing reads in a compressed binary format, including where each read maps on the reference genome. CRAM does the same job but compresses further by mainly storing differences from the reference instead of full sequences, making it smaller but reliant on having the matching reference genome available to decode it.

For our project, we'll likely use BAM for broader tool compatibility, while keeping CRAM in mind as a storage-saving option if space becomes tight.

---

# 7. Tumor-Normal Analysis

Tumor-normal analysis means sequencing two samples from the same patient — one from the tumor, one from healthy tissue — and comparing them directly.

## Why compare tumor against normal?

Every person's DNA already has thousands of natural, inherited variants (germline variants) that have nothing to do with cancer. If we only sequenced the tumor, we couldn't tell which variants are:

- Normal, inherited differences everyone has, or
- **Somatic mutations** — new changes that appeared specifically in the tumor cells.

By comparing tumor reads to normal reads at the same position, a caller can subtract out the inherited variants and flag only the ones that appear specifically in the tumor. This is the core idea behind "somatic" variant calling, as opposed to "germline" variant calling.

## Challenges specific to tumor-normal analysis

- Tumors are often a mix of cancer cells and normal cells ("tumor purity" issues), which can dilute the signal.
- Tumors can have subclones — different mutations in different parts of the same tumor.
- Sequencing and alignment errors can look like real mutations if not filtered carefully.

This is exactly why tools like Mutect2 and Strelka2 are built specifically for tumor-normal comparison rather than just single-sample variant calling.

### Source
- GATK — Mutect2 documentation
- Strelka2 — official User Guide

---

# 8. Variant Calling Tools Comparison

Bringing together what we found across Days 1–2:

| Tool | Type | Language | Best for | Needs matched normal? |
|---|---|---|---|---|
| **Mutect2 (GATK)** | Somatic SNV/indel caller | Java | Standard somatic calling, widely used and documented | Recommended, but supports tumor-only mode |
| **Strelka2** | Somatic + germline caller | C++ / Python | Fast, accurate calling with built-in rescoring | Yes, for somatic mode |
| **SomaticSeq** | Ensemble/ML combiner | Python / R | Combining results from multiple callers to reduce false positives | Uses whichever callers feed into it |
| **nf-core/sarek** | Full pipeline (not just a caller) | Nextflow, wraps multiple tools | Automating the entire FASTQ-to-annotated-VCF workflow | Supports tumor-normal pairs |

For our project, **Mutect2** remains the most practical starting choice — it's the most standard, best documented, and works well as a single tool rather than requiring us to set up an entire ensemble system like SomaticSeq.

### Source
- GATK — Mutect2 documentation
- Illumina Strelka2 — GitHub repository
- SomaticSeq — GitHub repository
- nf-core/sarek — GitHub repository

---

# 9. Annotation Databases

Once we have a filtered VCF, the variants by themselves are just coordinates and letters — they don't tell us anything about biological meaning. Annotation databases add that context. The main ones relevant to us:

- **dbSNP** — a large database of known genetic variants in the population, mostly used to flag whether a variant has been seen before.
- **gnomAD** — provides population allele frequencies, i.e., how common a variant is across large groups of people. Rare variants are generally more interesting for cancer analysis than common ones.
- **ClinVar** — reports known relationships between specific variants and diseases, including cancer.
- **COSMIC (Catalogue of Somatic Mutations in Cancer)** — specifically catalogs mutations that have been observed in real cancers, which makes it especially relevant for our project.
- **SIFT and PolyPhen** — tools/databases that predict whether a given amino-acid change is likely to damage protein function.

We won't need to build or host these databases ourselves — annotation tools like VEP already know how to pull from them.

### Source
- Ensembl VEP — Genome Biology, 2016
- Hunt et al. — "Annotating and prioritizing genomic variants using the Ensembl Variant Effect Predictor," Human Mutation, 2021

---

# 10. VEP and Annotation Workflow

## What is VEP?

VEP (Variant Effect Predictor) is a tool built by Ensembl that takes a VCF and figures out what each variant actually *does* — which gene and transcript it overlaps, what kind of change it causes (missense, stop-gained, frameshift, etc.), and whether it falls in a coding or regulatory region.

## How does it work, in simple terms?

1. VEP takes variant coordinates (from our VCF) as input.
2. It compares each variant against a set of known gene/transcript models (from Ensembl/GENCODE, or RefSeq).
3. For each variant, it reports which gene(s) and transcript(s) it overlaps, and predicts the "consequence" — for example, whether the change is missense (changes the amino acid), synonymous (doesn't change the amino acid), stop-gained (creates a premature stop), or something else.
4. If configured to, it also pulls in extra information from other databases — known variant IDs from dbSNP, population frequency from gnomAD, disease associations from ClinVar, and damage-prediction scores from tools like SIFT.
5. The output is either an annotated VCF or a tab-separated table, with one row per variant per affected transcript.

## How can we run it?

VEP can be run three ways: through a **web interface** (simplest, good for small numbers of variants), via a **REST API**, or as a **command-line tool** using a local "cache" of the annotation data (fastest and most reproducible for a real pipeline, since it doesn't need constant internet access once the cache is downloaded).

For our project, the command-line version makes the most sense — it fits into a Python-automated pipeline via `subprocess`, similar to how we planned to call Mutect2.

### Source
- Ensembl VEP — Genome Biology, 2016
- Hunt et al. — "Annotating and prioritizing genomic variants using the Ensembl Variant Effect Predictor," Human Mutation, 2021
- Ensembl VEP — official documentation and tutorial

---

# 11. Data Size and Computing Requirements

Putting together what this means practically for us:

- A **full WGS FASTQ file** for one sample can be tens of GB; a tumor-normal WGS pair (like full SEQC2) can be well over 100 GB combined.
- A **single-chromosome or exome-region BAM subset** is realistically in the hundreds of MB to low GB range — something a normal laptop can store and process.
- **VEP annotation** is comparatively lightweight — a single run typically takes a few minutes and a few GB of memory per sample, according to published pipeline benchmarks, which is very manageable.
- **Variant calling** (Mutect2/Strelka2) is the more compute-intensive step, especially across a full genome — this is one more reason to restrict ourselves to a chromosome or exome subset rather than the whole genome.
- **Reference genome files**, if restricted to one chromosome, are only a small fraction of the full ~3 GB human genome.

Overall, as long as we stick to a small regional subset rather than a full genome, the whole pipeline (alignment already done → calling → filtering → annotation → reporting) should be realistic to run on a normal laptop within our three-week timeframe.

### Source
- Scalable Runtime Architecture for Data-driven, Hybrid HPC and ML Workflow Applications (VEP runtime/memory benchmarks)
- NVIDIA Parabricks — SEQC2 tutorial documentation

---

# 12. Dataset Selection for Our Prototype

Bringing Day 3 and today's research together, our selection criteria and decision stay consistent:

**Chosen dataset: a small subset (single chromosome or exome region) of the SEQC2 HCC1395/HCC1395BL tumor-normal pair, using BAM files rather than raw FASTQ.**

This satisfies our dataset requirements from Section 3:

- Real tumor + matched normal pair ✔
- Standard format (BAM/VCF) ✔
- Has a published truth set for evaluation ✔
- Fully open access, no approval process ✔
- Small enough for a normal computer, once subset ✔
- Well documented, widely used in tutorials and benchmarking papers ✔

If we need an even lighter option purely for early testing of our scripts before working with real data, small GATK/Galaxy tutorial test files remain a good fallback.

---

# 13. Data Privacy and Licensing

Even though our chosen dataset is open access, it's worth understanding the wider landscape, since other cancer datasets we looked at are not.

## Why cancer genomic data is sensitive

Genomic sequence data is considered potentially identifying — unlike a name or address, DNA can't really be "anonymized" the way other personal data can, since it's inherently unique to a person (aside from identical twins). Because of this, most real-patient cancer datasets are treated as sensitive health information.

## Main frameworks that apply

- **HIPAA (US)** — governs Protected Health Information. Genomic data counts as PHI when it can be linked to an identifiable person; de-identified data falls outside HIPAA's scope, but genomic de-identification is genuinely hard to guarantee.
- **GDPR (EU)** — genomic data can count as personal data under GDPR, which requires specific safeguards, informed consent, and purpose limitation for anyone processing data linked to EU individuals.
- **dbGaP (NIH, US)** — the main controlled-access system for datasets like TCGA. Access requires a formal Data Access Request and a Data Use Certification, reviewed by a Data Access Committee, and can take time to be approved.
- **DACO (ICGC ARGO)** — a similar controlled-access review process for ICGC data, requiring institutional review and, in some cases, ethics approval.

## What this means for our project

Because SEQC2's HCC1395 dataset comes from cell lines specifically established and distributed for open research and benchmarking (not from an identifiable patient's clinical record in the way TCGA data is), it's distributed openly without needing dbGaP-style approval. We should still cite the dataset properly and stick to its intended research/benchmarking use, but we don't need to go through a formal data access application for this project.

If, later on, we ever wanted to extend the project to a controlled-access dataset like TCGA, that would require dbGaP approval, institutional affiliation, and a Data Use Certification — something well outside the scope of a three-week project.

### Source
- NIH Genomic Data Sharing Policy — genome.gov
- dbGaP Controlled Data Access documentation
- Genomic Data Sharing and HIPAA — compliance overview
- Google Cloud Whitepaper — Handling genomic data in the cloud (GDPR/HIPAA overview)
- Becnel et al. — "An open access pilot freely sharing cancer genomic data from participants in Texas," Scientific Data, 2016

---

# 14. Day 4 Conclusion

Today's research filled in the pieces around our core pipeline: what a reference genome is and why it has to match our data exactly, how tumor-normal comparison actually isolates somatic mutations, how annotation tools like VEP turn raw variant coordinates into biological meaning, and — importantly — why data access and privacy rules exist and how they shape which datasets are realistic for a short project.

Combined with Day 3, we now have a full, justified answer for our dataset question: a small, open-access subset of SEQC2 HCC1395/HCC1395BL, aligned to a matching reference genome build, run through Mutect2, filtered, annotated with VEP, and turned into a report. Every piece of that plan is now backed by a specific reason rather than a guess — which sets us up well to actually start building in Week 2.

---

# Sources

- NCI Genomic Data Commons — About GDC and GDC documentation
- SEQC2 / Nature Biotechnology
- ICGC ARGO — Data Access documentation
- NIST Genome in a Bottle Consortium
- Texas Cancer Research Biobank — Open Access pilot, Scientific Data, 2016
- bcbio_validation_workflows — GitHub repository
- Genome Reference Consortium — GRCh37/GRCh38 documentation
- SAMtools / GA4GH — alignment format specifications
- GATK — Mutect2 documentation
- Illumina Strelka2 — GitHub repository and User Guide
- SomaticSeq — GitHub repository
- nf-core/sarek — GitHub repository
- Ensembl VEP — Genome Biology, 2016
- Hunt et al. — "Annotating and prioritizing genomic variants using the Ensembl Variant Effect Predictor," Human Mutation, 2021
- Ensembl VEP — official documentation and tutorial
- Scalable Runtime Architecture for Data-driven, Hybrid HPC and ML Workflow Applications
- NVIDIA Parabricks — SEQC2 tutorial documentation
- NIH Genomic Data Sharing Policy — genome.gov
- dbGaP Controlled Data Access documentation
- Genomic Data Sharing and HIPAA — compliance overview
- Google Cloud Whitepaper — Handling genomic data in the cloud
```