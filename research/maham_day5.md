
# Cancer Variant Calling and Annotation Pipeline

## Day 5 Research — Variant Filtering (Summary)

**Team Member:** Maham
**Project Type:** Python / AI
**Research Phase:** Week 1 - Day 5
**Date:** 20 August 2026

---

# 1. Why Filtering Is Needed

Variant callers like Mutect2 are built to be sensitive — they'd rather flag a possible mutation and let us double-check it than miss a real one. Because of this, the raw VCF a caller produces is full of noise: sequencing errors, alignment artifacts, and low-confidence calls sitting right alongside real mutations.

Filtering is the step where we separate the two. Without it, our downstream annotation and priority-scoring steps would be spending effort on garbage variants, and our final report would be misleading. Filtering isn't optional — it's what turns "everything the caller noticed" into "what we can actually trust."

### Source
- GATK — Hard-filtering germline short variants
- GATK — FilterMutectCalls documentation

---

# 2. Common Filtering Criteria

- **QUAL** — the caller's own confidence score for the variant as a whole. Low QUAL usually means weak statistical support. Common practice is to require QUAL above some threshold (often 20–30+), though the "correct" cutoff varies by caller and dataset — there's no single universal number.
- **DP (Depth)** — how many reads covered that position. A variant seen in only 2–3 reads out of thousands is much less trustworthy than one seen in 30+ reads. Low-depth positions are usually filtered out or flagged (a common rule of thumb is requiring DP ≥ 10).
- **AF (Allele Frequency)** — what fraction of reads at that position support the alternate allele. In somatic calling, very low AF can mean a real but rare subclonal mutation, or it can mean sequencing noise — so AF is often combined with DP rather than judged alone.
- **QD (Quality by Depth)** — QUAL normalized by depth, used so that very high-depth positions don't get an artificially inflated quality score.
- **FS (Fisher Strand) / SOR (Strand Odds Ratio)** — flag strand bias, where a variant appears mostly on one strand of reads (forward or reverse) rather than both — a common sign of a sequencing artifact rather than a real mutation.
- **MQ (Mapping Quality)** — how confidently the reads themselves were aligned to that spot. Low MQ means the reads might not really belong there.
- **Orientation bias filters (for cancer specifically)** — FFPE-preserved tumor samples commonly produce artificial C>T and G>T changes from chemical damage, not real mutations. GATK has specific tools (`CollectSequencingArtifactMetrics` / `FilterByOrientationBias`) to catch and remove these.
- **Panel of Normals (PoN) / population frequency** — variants that show up recurrently across unrelated normal samples, or that are common in population databases like gnomAD, are usually sequencing artifacts or germline variants rather than real somatic mutations, and get filtered out.

### Source
- GATK — Hard-filtering germline short variants
- GATK — VariantFiltration tool documentation
- GATK — FilterMutectCalls documentation
- De Summa et al. — "GATK hard filtering: tunable parameters..." BMC Bioinformatics, 2017

---

# 3. How Low-Quality Variants Get Removed Before Annotation

The general process is:

1. **Run the caller** (Mutect2) to get a raw VCF — this includes both real and false-positive calls.
2. **Apply filtering criteria** using QUAL, DP, AF, QD, strand bias, mapping quality, and orientation-bias checks.
3. **Mark variants in the FILTER column** — instead of deleting variants outright, filtering tools usually tag each variant with a filter name (or `PASS` if it passed everything). This keeps a record of *why* something was flagged, which is useful for review.
4. **Select only PASS variants** for the next step, using a tool like `SelectVariants` or `bcftools view -f PASS`, so annotation and reporting only work with the trustworthy subset.

This "flag, then select" approach is preferred over silently deleting variants, because it keeps the process transparent and reversible — if a threshold turns out to be too strict, nothing is permanently lost.

### Source
- GATK — VariantFiltration tool documentation
- GATK — "(How to) Filter variants either with VQSR or by hard-filtering"

---

# 4. Using GATK for Filtering

For **somatic** variants specifically (our case), GATK's own recommended path is:

    gatk Mutect2 -R reference.fa -I tumor.bam -I normal.bam -O raw.vcf
    gatk FilterMutectCalls -R reference.fa -V raw.vcf -O filtered.vcf

`FilterMutectCalls` is purpose-built for Mutect2 output — it applies a set of statistical filters tuned for somatic calling (including checks related to strand bias and low allele fraction) and writes the result into the FILTER column.

For more general **hard filtering** (setting our own thresholds), GATK's `VariantFiltration` tool is used instead, with expressions like:

    gatk VariantFiltration \
      -R reference.fa \
      -V raw.vcf \
      -O filtered.vcf \
      --filter-name "QD_filter" --filter-expression "QD < 2.0" \
      --filter-name "FS_filter" --filter-expression "FS > 60.0" \
      --filter-name "MQ_filter" --filter-expression "MQ < 40.0" \
      --genotype-filter-name "DP_filter" --genotype-filter-expression "DP < 10"

Each expression adds its own label to the FILTER field if a variant fails it, so multiple issues can be tracked per variant instead of just a single pass/fail flag.

### Source
- GATK — FilterMutectCalls documentation
- GATK — VariantFiltration documentation
- GATK — Hard-filtering germline short variants

---

# 5. Using BCFtools for Filtering

`bcftools` is a lighter, faster command-line alternative, useful for quick filtering without needing the full GATK setup. A typical use:

    bcftools view -i 'QUAL>30 && INFO/DP>10 && INFO/AF>0.05' raw.vcf.gz -O z -o filtered.vcf.gz

Or, to just keep variants already marked PASS by an upstream tool like FilterMutectCalls:

    bcftools view -f PASS filtered.vcf.gz -O z -o pass_only.vcf.gz

`bcftools filter` (as opposed to `view -i`) can also be used to *add* new FILTER tags based on an expression, similar in spirit to GATK's VariantFiltration, without removing rows outright.

For our project, `bcftools` is a practical lightweight option for quick, script-friendly filtering inside our Python pipeline (called via `subprocess`), while `FilterMutectCalls` remains the more "official" first pass right after variant calling.

### Source
- SAMtools/BCFtools — official documentation
- GATK — FilterMutectCalls documentation

---

# 6. Summary — Key Points

- Raw variant caller output is deliberately over-sensitive and needs filtering before it's usable.
- The main criteria we'll use: **QUAL**, **DP**, **AF**, plus strand-bias and mapping-quality checks; for tumor data specifically, orientation-bias (FFPE artifact) filtering matters too.
- Filtering marks variants with a reason in the FILTER column rather than deleting them outright — we then keep only the `PASS` variants going forward.
- **GATK's `FilterMutectCalls`** is the standard first step right after Mutect2; **`VariantFiltration`** is used for custom hard-filtering with our own thresholds.
- **`bcftools`** is a faster, simpler alternative for filtering and is easy to call from Python.
- This filtered, PASS-only VCF is what should be handed off to VEP for annotation — filtering always comes before annotation in our pipeline order.

---

# Sources

- GATK — Hard-filtering germline short variants
- GATK — FilterMutectCalls documentation
- GATK — VariantFiltration tool documentation
- GATK — "(How to) Filter variants either with VQSR or by hard-filtering"
- De Summa et al. — "GATK hard filtering: tunable parameters to improve variant calling for next generation sequencing targeted gene panel data," BMC Bioinformatics, 2017
- SAMtools/BCFtools — official documentation
```