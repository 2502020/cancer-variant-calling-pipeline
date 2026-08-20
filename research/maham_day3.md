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

Since we're working with limited computer resources, CRAM is worth knowing about — it can shrink storage requirements significantly. But BAM is still the more universally supported format, so a lot of tutorials, tools, and public test data use BAM by default. We'll likely work mainly with BAM (