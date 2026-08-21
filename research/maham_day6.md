
# Cancer Variant Calling and Annotation Pipeline

## Day 6 Research — Testing Strategy and Evaluation Plan

**Team Member:** Maham
**Project Type:** Python / AI
**Research Phase:** Week 1 - Day 6
**Date:** 21 August 2026

---

# 1. Pipeline Testing Strategy

Since our pipeline has several connected stages (alignment → variant calling → filtering → annotation → reporting), we can't just test the final output and assume everything upstream worked correctly. If something goes wrong early on, it can quietly produce wrong-looking-right results further down the line.

Our overall strategy is to test **at every stage**, not just at the end:

- Check that each stage's output looks reasonable *before* feeding it into the next stage.
- Use small, known test data first, where we can predict roughly what the output should look like.
- Compare our final results against a published truth set, not just check that the pipeline "ran without crashing."
- Keep a simple log of what passed/failed at each stage, so problems can be traced back to their source instead of just showing up as a strange final report.

### Source
- SIB Swiss Institute of Bioinformatics — NGS variant analysis training materials

---

# 2. Test Datasets and Test Cases

We're planning two tiers of test data:

- **Tiny sanity-check data** — small GATK/Galaxy tutorial files (a few MB), used purely to check that our scripts run correctly and each tool is called with the right arguments. These won't tell us much about accuracy, just that the pipeline mechanically works.
- **Real benchmark data** — our chosen SEQC2 HCC1395/HCC1395BL subset, which comes with a published high-confidence truth VCF. This is what we'll use to actually measure accuracy.

Test cases we want to cover:

- A **normal run** — a region we expect to contain real somatic variants.
- An **edge case** — a region with very low coverage, to see how the pipeline handles thin data.
- A **negative case** — a region known to have no somatic variants (or only germline ones), to check the pipeline doesn't just report false positives everywhere.
- A **malformed input case** — e.g., a BAM file with a missing index, to see whether the pipeline fails gracefully or just crashes without explanation.

---

# 3. Testing FastQC Results

If we do end up starting from raw FASTQ at any point, FastQC is the standard tool for checking the quality of reads before doing anything else with them. We'd be checking:

- **Per-base sequence quality** — quality scores shouldn't drop off badly across the read.
- **Per-sequence GC content** — should roughly match the expected GC content for human DNA; a strange spike can mean contamination.
- **Adapter content** — leftover sequencing adapters should be minimal, or need trimming before alignment.
- **Overrepresented sequences** — a high count of one repeated sequence can indicate contamination or a technical artifact.

Since we're planning to start from already-aligned BAM files instead of raw FASTQ (as decided in Day 3–4), FastQC won't be a core part of our own pipeline run, but it's still useful to know how to read its output in case we ever need to sanity-check the underlying SEQC2 FASTQ data.

### Source
- Galaxy Training Network — FASTQ format and quality control resources

---

# 4. Testing Alignment Results

For alignment (or for checking already-aligned BAM files), the standard sanity checks are:

- **`samtools flagstat`** — gives a quick summary: total reads, how many mapped, how many were properly paired, duplicate rate. A very low mapping percentage is a red flag.
- **Coverage/depth check** — using `samtools depth` or similar, to confirm the region we're working with actually has reasonable read coverage (matching what we expect for our chosen subset).
- **Mapping quality distribution** — most reads should have high mapping quality (MAPQ); a lot of low-MAPQ reads suggests ambiguous or repetitive regions.
- **Reference match check** — confirming the BAM file's reference genome build matches the one we intend to use downstream (a mismatch here silently corrupts every later step).

### Source
- SAMtools / GA4GH — SAM/BAM specifications

---

# 5. Testing Variant Calling Results

Before even comparing to a truth set, there are basic sanity checks on Mutect2's raw output:

- Does the raw VCF have a **reasonable number of variants** for the size of the region we're testing? Wildly too many or too few is a warning sign.
- Are there both **SNVs and indels** represented, roughly in the proportions we'd expect (SNVs are usually much more common than indels)?
- Do QUAL, DP, and AF values fall in **sensible ranges**, rather than being all zero or all identical (a sign something upstream broke)?
- Does the tumor sample show variants that the normal sample doesn't (confirming the tool is actually distinguishing tumor-specific mutations, not just calling every difference from the reference)?

These are "does this look broken" checks — the real accuracy check comes later, against the truth set.

---

# 6. VCF Validation

Beyond checking the biology, we also need to check that the VCF file itself is technically well-formed:

- **Format validation** — confirming the file has a proper header, correct column structure, and follows VCF spec (tools like `bcftools view` or `vcf-validator` will complain loudly if the file is malformed).
- **Sorted and indexed** — VCF files need to be coordinate-sorted and indexed (`.tbi`/`.csi`) for most downstream tools to use them efficiently.
- **Consistent sample naming** — making sure the tumor and normal sample columns are correctly labeled and in the expected order, since downstream scripts will assume a specific column layout.
- **No duplicate or overlapping records** at the same position, which can confuse annotation tools.

This step matters because a lot of downstream failures in real pipelines come from a technically invalid VCF, not from a biological error.

### Source
- SAMtools / GA4GH — VCF specifications

---

# 7. Testing Variant Annotation

After running VEP, we want to check:

- Every variant in the filtered VCF actually **received an annotation** — unannotated rows likely mean a coordinate mismatch (e.g., wrong reference genome build) between our VCF and VEP's cache.
- The **gene names** reported make sense for the region we're testing (if we know our test region overlaps a specific gene, we should see that gene name appear).
- **Consequence types** (missense, synonymous, stop-gained, etc.) are being reported and look plausible, not defaulting to "unknown" everywhere.
- If we've enabled extra annotation sources (dbSNP, gnomAD, ClinVar), spot-check a few known variants to see if their known IDs/frequencies show up correctly.

### Source
- Ensembl VEP — official documentation and tutorial

---

# 8. Testing Variant Filtering

To check our filtering step is actually doing what we expect:

- Compare the **variant count before and after filtering** — if filtering removes almost nothing, our thresholds are probably too loose; if it removes almost everything, they're probably too strict.
- Spot-check a few variants marked as failing a filter (e.g., low DP) and confirm their actual DP value in the VCF really is below our threshold — this catches bugs in the filter expression itself.
- Confirm that **PASS-only variants** are what actually get passed to annotation, not the full unfiltered set by mistake.
- Check filtering behaves consistently between test runs on the same input (i.e., it's deterministic, not accidentally dependent on file order or system state).

---

# 9. Accuracy and Correctness of Results

This is where we move from "does it run" to "is it right." The standard approach in the field is to compare our final variant calls against the SEQC2 truth set using precision, recall, and F1 score:

- **Precision** — of the variants we called, what fraction were actually real (true positives ÷ all variants we called).
- **Recall (sensitivity)** — of the real variants that exist, what fraction did we successfully find (true positives ÷ all real variants).
- **F1 score** — the harmonic mean of precision and recall, giving one combined number that penalizes being either too aggressive (low precision) or too conservative (low recall).

The standard tool for this kind of comparison is **hap.py**, often paired with RTG's **vcfeval** as the underlying comparison engine — this is the approach recommended by the GA4GH benchmarking group and used in most published variant-calling benchmarking papers. It compares our VCF against a truth VCF (and, ideally, a "high-confidence regions" BED file) and reports true positives, false positives, false negatives, precision, recall, and F1, split out separately for SNVs and indels.

For our project, running our filtered/annotated VCF through hap.py against the SEQC2 truth set is the main way we'll be able to say "our pipeline actually works," rather than just "our pipeline produces a file."

### Source
- Illumina/hap.py — GitHub repository and documentation
- Krishnan et al. — "Benchmarking workflows to assess performance and suitability of germline variant calling pipelines in clinical diagnostic assays," BMC Bioinformatics, 2021
- Sebby — "Demystifying benchmarking: A guide to germline variant calling metrics," Truwl/Medium

---

# 10. Performance: Time and Memory Usage

Since we're working on a normal computer with a small dataset subset, we also want to track basic performance, both to catch problems and to report honestly on our project's limitations:

- **Wall-clock time per stage** — how long alignment (if run), variant calling, filtering, and annotation each take. Simple to track with Python's `time` module wrapped around each `subprocess` call.
- **Peak memory usage** — tools like Mutect2 can be memory-hungry; tracking peak RAM per stage helps us understand whether our chosen region size is realistic for the hardware we have.
- **Scaling check** — running the pipeline on two differently-sized test regions (e.g., a small gene region vs. a full chromosome) to see roughly how time/memory scale, which helps us honestly state what our pipeline could and couldn't handle at larger scale.

This isn't about optimizing for speed — it's about being able to say clearly, in our final report, what hardware and data size our pipeline was actually tested on.

---

# 11. Error Handling and Failure Cases

We want our pipeline to fail *usefully* rather than just crash with a cryptic stack trace. Cases we plan to test deliberately:

- **Missing or misnamed input files** — does our Python wrapper give a clear error message, or does it just fail deep inside a subprocess call?
- **Mismatched reference genome** — feeding in a BAM aligned to a different genome build than the one we're using downstream, to confirm we catch this rather than silently producing wrong coordinates.
- **Empty VCF** — what happens if a region genuinely has zero variants? The pipeline should handle this gracefully and say so in the report, not error out.
- **Tool not installed / not on PATH** — since our Python layer calls external tools via `subprocess`, we want a clear message if, say, VEP isn't available, rather than a generic `FileNotFoundError`.

### Source
- Python Documentation — `subprocess`

---

# 12. Comparison with Existing Tools/Pipelines

To put our own results in context, we plan to compare our pipeline's output (accuracy, and roughly, runtime) against at least one reference point:

- Running the **same test data through Mutect2 alone with GATK's standard FilterMutectCalls** (essentially, the "official" recommended path) and comparing precision/recall against our own filtering choices.
- If time allows, comparing against results from an established pipeline like **nf-core/sarek** run on the same subset, to see how close our smaller, simpler pipeline gets to a full production-grade one.

The point of this isn't to "beat" existing tools — as we noted back in Day 2, that's not realistic in three weeks. It's to demonstrate that our simpler pipeline produces results in the same ballpark as established tools, which supports the idea that a smaller, more understandable pipeline can still be scientifically reasonable.

---

# 13. Final Evaluation Criteria

Bringing everything together, here's how we plan to judge whether our pipeline is "good enough" by the end of the project:

- **Correctness** — F1 score against the SEQC2 truth set above some reasonable threshold (exact target still to be decided once we see baseline numbers).
- **Robustness** — pipeline runs cleanly on all our test cases (normal, low-coverage, no-variant, malformed input) without silent failures.
- **Transparency** — every filtered-out variant and every priority score has a traceable reason behind it, not a black-box result.
- **Feasibility** — the whole pipeline runs in a reasonable amount of time and memory on a normal computer, using our chosen data subset.
- **Reporting quality** — the final report clearly communicates what was tested, on what data, and what the accuracy numbers actually mean (including honest limitations).

---

# 14. Day 6 Conclusion

Today's research shifted our focus from *building* the pipeline to *proving it works*. The main takeaway is that testing needs to happen at every stage, not just at the very end — a problem in alignment or filtering can easily hide inside a final report that still looks fine on the surface.

The most important finding is that there's already a standard, well-established way to measure variant-calling accuracy: comparing our output against a truth set using **hap.py/vcfeval** to get precision, recall, and F1 score. This gives us an honest, field-standard way to say how good our pipeline actually is, rather than just showing that it runs. Combined with basic performance tracking, error-handling checks, and a comparison against GATK's standard workflow, we now have a full testing and evaluation plan to apply once the pipeline itself is built in Week 2.

---

# Sources

- SIB Swiss Institute of Bioinformatics — NGS variant analysis training materials
- Galaxy Training Network — FASTQ format and quality control resources
- SAMtools / GA4GH — SAM, BAM and VCF specifications
- Ensembl VEP — official documentation and tutorial
- Illumina/hap.py — GitHub repository and documentation
- Krishnan et al. — "Benchmarking workflows to assess performance and suitability of germline variant calling pipelines in clinical diagnostic assays," BMC Bioinformatics, 2021
- Sebby — "Demystifying benchmarking: A guide to germline variant calling metrics," Truwl/Medium
- Python Documentation — subprocess
- GATK — FilterMutectCalls documentation
- nf-core/sarek — GitHub repository
```