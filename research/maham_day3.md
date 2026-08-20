
# Cancer Variant Calling and Annotation Pipeline

## Day 3 Research — File Formats, Public Datasets, and Project Input/Output

**Team Member:** Maham
**Project Type:** Python / AI
**Research Phase:** Week 1 - Day 3
**Date:** 18 August 2026

---

# 1. FASTQ — What It Is and What It Contains

FASTQ is a plain-text file format used to store raw sequencing reads and their quality scores. It is normally the very first file we deal with in a sequencing pipeline, straight off the sequencing machine.

Each read is stored using four lines:

- **Line 1:** Read identifier — starts with `@`, and contains info like the instrument name, run number, and read number.
- **Line 2:** The actual DNA sequence (A, T, C, G, and sometimes N for unknown bases).
- **Line 3:** A `+` separator line, sometimes repeating the identifier.
- **Line 4:** Quality scores — one character per base, encoding how confident the machine was about that base call.

Example of one read:

    @SEQ_ID_001
    GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCC
    +
    !''*((((***+))%%%++)(%%%%).1***-+*''))**

The quality scores are usually written using a scheme called Phred quality scores, where each character corresponds to a probability that the base call is wrong. A higher score means the machine was more confident.

A single sequencing run can produce millions of these four-line reads, and a FASTQ file for a full genome can be tens of gigabytes in size.

### Source
- Galaxy Training Network — FASTQ format
- EMBL-EBI — Sequencing experiments

---

# 2. BAM and CRAM — What They Are and How They Differ

## What is BAM?

BAM (Binary Alignment/Map) is the compressed, binary version of SAM (Sequence Alignment/Map). Once reads from a FASTQ file are aligned to a reference genome, the alignment results — where each read maps, how well it matches, any mismatches — are stored in BAM format.

A BAM file basically tells us, for every read: which chromosome it came from, what position it starts at, its mapping quality, and its actual sequence and quality scores (carried over from the FASTQ).

## What is CRAM?

CRAM is a newer, more compressed alternative to BAM. It stores the same kind of alignment information, but instead of storing the full DNA sequence for every read, it mainly stores the **differences** between the read and the reference genome it was aligned to.

Because most of a read matches the reference exactly, CRAM only needs to record the parts that don't match. This makes CRAM files noticeably smaller than BAM files for the same data — often 30–60% smaller, depending on the settings used.

## Main differences between BAM and CRAM

| Feature | BAM | CRAM |
|---|---|---|
| Storage basis | Stores full read sequences | Stores mainly differences from the reference |
| File size | Larger | Smaller (better compression) |
| Reference genome needed | Not required to read the file | Usually required to fully decode the file |
| Tool support | Supported by almost all tools | Supported by most modern tools (samtools, GATK, etc.) |
| Common use | Still very common, especially in older pipelines | Increasingly used for long-term storage to save space |

## Why does this matter for our project?

Since we're working with limited computer resources, CRAM is worth knowing about — it can shrink storage requirements significantly. But BAM is still the more universally supported format, so a lot of tutorials, tools, and public test data use BAM by default. We'll likely work mainly with BAM (or a small BAM subset) for compatibility, and can mention CRAM as a space-saving option.

### Source
- SAMtools / GA4GH — SAM/BAM/CRAM format specifications

---

# 3. VCF — What It Is and What Its Important Columns Mean

VCF (Variant Call Format) is a text-based format used to store the genetic variants found after variant calling. It's the main output of tools like Mutect2, and it's also the main *input* format for filtering, annotation, and prioritization steps.

A VCF file has two parts:

- A **header section** (lines starting with `##`) describing the file, the tools used, and what each field means.
- A **data section**, where each row is one variant.

## Main columns in a VCF

| Column | What it means |
|---|---|
| **CHROM** | Which chromosome the variant is on (e.g., chr1, chr17) |
| **POS** | The position on the chromosome where the variant starts |
| **ID** | An identifier for the variant, if known (e.g., an rsID from dbSNP). Often just `.` if unknown |
| **REF** | The reference base(s) at that position |
| **ALT** | The alternate (variant) base(s) found in the sample |
| **QUAL** | A quality score showing how confident the caller is that this is a real variant |
| **FILTER** | Whether the variant passed quality filters — `PASS` means it passed; anything else names the filter it failed |
| **INFO** | Extra details about the variant as a whole — things like read depth, allele frequency, or caller-specific stats |
| **FORMAT** | Lists which fields are given per-sample (e.g., genotype, depth) |
| **SAMPLE (one column per sample)** | The actual values for the fields listed in FORMAT, for each sample (e.g., tumor, normal) |

### Example (simplified)

    #CHROM  POS      ID   REF  ALT  QUAL  FILTER  INFO         FORMAT   TUMOR
    chr17    7577121  .    C    T    87.3  PASS    DP=62;AF=0.31 GT:AD:DP  0/1:43,19:62

This row means: on chromosome 17, position 7577121, the reference base C changed to T in the tumor sample, with 62 reads covering that position and about 31% of them showing the variant.

For our project, QUAL, FILTER, and the INFO/FORMAT depth and allele-frequency fields are especially important — they're the raw material we'll use for filtering and, later, for building features for the priority-scoring model.

### Source
- NCI Genomic Data Commons — VCF documentation
- SAMtools / GA4GH — VCF specifications

---

# 4. Where to Get Public Cancer Genomic Datasets

There are a handful of major places researchers get public cancer sequencing data from:

- **SEQC2 (Sequencing Quality Control Phase 2) / HCC1395 dataset** — a benchmarking dataset built specifically for testing somatic variant calling, with a matched tumor and normal cell line and a published "truth set" of confirmed mutations. Hosted through NCBI SRA and SEQC2 project resources.
- **NCI Genomic Data Commons (GDC) / TCGA (The Cancer Genome Atlas)** — a huge repository of tumor sequencing data across 33+ cancer types. Some processed data (like MAF variant summaries) is open access, but raw sequencing reads (BAM/FASTQ) usually require controlled access approval (dbGaP), since they come from real patients.
- **ICGC ARGO (formerly the ICGC Data Portal)** — another large international cancer genomics resource. The original open web portal has been retired; most current data now requires DACO (Data Access Compliance Office) approval, which involves an application and institutional review.
- **Genome in a Bottle (GIAB)** — not cancer-specific, but provides very well-characterized reference genomes (like NA12878) with high-confidence "truth" variant sets. Useful for testing pipeline correctness even without real tumor data.
- **1000 Genomes Project** — population-scale germline sequencing data, freely available. Good for practicing alignment/variant-calling basics, but not built for somatic (tumor-vs-normal) analysis.
- **Community-curated subsets** (e.g., the bcbio validation workflows on GitHub) — small, pre-trimmed pieces of larger datasets (like a single chromosome or exome region) specifically prepared for testing pipelines on modest hardware.

### Source
- SEQC2 / Nature Biotechnology
- NCI Genomic Data Commons — GDC documentation
- ICGC ARGO — Data Access documentation
- NIST Genome in a Bottle Consortium
- 1000 Genomes Project
- bcbio_validation_workflows — GitHub repository

---

# 5. Comparing Suitable Datasets

| Dataset | Format available | Approx. size | Access | Runs on a normal computer? |
|---|---|---|---|---|
| **SEQC2 HCC1395 (full WGS)** | FASTQ, BAM, VCF | ~65 GB per file; ~130 GB for the tumor-normal pair | Fully open access, no application needed | No — too large to download or process locally |
| **SEQC2 HCC1395 (small subset, e.g. one chromosome or exome region)** | BAM, VCF | A few hundred MB to a few GB, depending on the region chosen | Open access (subset created by us or by the community from the open full dataset) | Yes — realistic for a laptop |
| **TCGA / GDC raw sequencing data** | FASTQ, BAM | Very large (part of a >400 TB collection) | Controlled access (dbGaP approval required) | No — both access and size are barriers |
| **TCGA / GDC processed variant summaries (MAF)** | MAF / tabular | Small (MBs) | Open access | Yes, but this is already-called variants, not raw reads — not useful for practicing the calling step |
| **ICGC ARGO** | VCF, BAM (varies by project) | Varies, often large | Mostly controlled access (DACO approval), some open-access files | Depends — approval process alone makes this unrealistic in 3 weeks |
| **Genome in a Bottle (NA12878, chr20 subset)** | FASTQ, BAM, VCF | A few hundred MB for a single-chromosome subset | Fully open access | Yes |
| **1000 Genomes (subset)** | FASTQ, BAM, VCF | Varies, small if subset to one region | Fully open access | Yes, but germline only — no tumor/normal comparison |
| **bcbio validation exome/chr20 subsets** | FASTQ, BAM, VCF (truth set included) | Small, purpose-built for testing (order of hundreds of MB) | Fully open access | Yes |

### What stands out

- The full SEQC2 dataset is the most scientifically relevant (it's a real tumor/normal pair with a published truth set), but far too large to use as-is.
- TCGA and ICGC ARGO are mostly locked behind institutional approval for raw data, which we don't have time to apply for and wait on in a 3-week project.
- The realistic path is to use a **small, regional subset** of an open-access dataset that still has a reference truth set to check our results against.

---

# 6. Recommended Dataset

**Recommendation: A small subset of the SEQC2 HCC1395 / HCC1395BL dataset, limited to one chromosome or a targeted exome region, using the already-aligned BAM files rather than raw FASTQ.**

Reasons:

- It's a real tumor and matched normal sample, so it actually represents the kind of somatic variant-calling problem our project is about.
- It comes with a published high-confidence "truth" variant set, so we can check whether our pipeline's output is scientifically sensible — not just whether the code runs without errors.
- It's fully open access — no DACO application, no dbGaP approval, no waiting period.
- By downloading only a subset (one chromosome, such as chr20 or chr17, or a limited exome region) instead of the full ~130 GB pair, the data becomes small enough to store and process on a normal laptop.

As a fallback or for early testing before downloading the subset, we can also use small GATK/Galaxy tutorial test files (a few MB) just to make sure our scripts and pipeline logic work, before running on the real SEQC2 subset.

### Source
- SEQC2 / Nature Biotechnology
- NVIDIA Parabricks — SEQC2 tutorial documentation

---

# 7. Deciding Our Project's Input and Output

## Input

- A **tumor BAM file** and a **matched normal BAM file**, both limited to a single chromosome or small region (from the SEQC2 subset).
- A **reference genome** file matching that same region (so alignment coordinates line up).
- (Optional, for evaluation only) The **truth VCF** for that region, used just to check our pipeline's accuracy — not fed into the pipeline itself.

## Output

- A **raw VCF** from the variant-calling step (Mutect2).
- A **filtered VCF** after removing low-confidence calls.
- An **annotated variant table** (CSV, built with pandas) containing columns like Gene, Chromosome, Position, REF, ALT, Quality, Depth, Allele Frequency, and Effect.
- A **priority-scored version** of that table, once the ML component is added, ranking variants from most to least likely to be biologically important — along with a short explanation of why each variant got its score.
- A final **human-readable report** (HTML or Markdown) summarizing: total variants found, how many passed filtering, variant types (SNVs vs indels), top genes affected, the highest-priority variants, and a few simple graphs (e.g., variants per chromosome, SNVs vs indels).

## Overall flow with this input/output in mind

**Tumor + Normal BAM (chr subset) → Mutect2 → Raw VCF → FilterMutectCalls → Filtered VCF → Annotation → pandas table (CSV) → ML priority scoring → Report (HTML/Markdown with graphs)**
--- 

### Main thing I learned

The biggest real-world constraint on this project isn't the code — it's data size and data access. Full cancer genomics datasets are either too large to store locally or require formal approval that takes longer than three weeks to get. The practical solution is to use a small, open-access subset of a well-documented dataset (like SEQC2 HCC1395) that still comes with a truth set, so we can actually evaluate whether our pipeline works — not just whether it runs.

---

# Sources

- Galaxy Training Network — FASTQ format
- EMBL-EBI — Sequencing experiments
- SAMtools / GA4GH — SAM, BAM, CRAM and VCF specifications
- NCI Genomic Data Commons — VCF documentation and GDC documentation
- SEQC2 / Nature Biotechnology
- NVIDIA Parabricks — SEQC2 benchmarking tutorial documentation
- ICGC ARGO — Data Access documentation
- NIST Genome in a Bottle Consortium
- 1000 Genomes Project
- bcbio_validation_workflows — GitHub repository
```