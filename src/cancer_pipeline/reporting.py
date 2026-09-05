import os

def generate_report(input_vcf: str, output_report: str = "results/report/final_report.txt") -> bool:
    """
    Generate a human-readable summary report from an annotated VCF.
    Returns True if successful, False otherwise.
    """
    os.makedirs(os.path.dirname(output_report), exist_ok=True)

    try:
        variants = []
        with open(input_vcf, "r") as infile:
            for line in infile:
                if line.startswith("#"):
                    continue
                fields = line.strip().split("\t")
                chrom, pos, ref, alt, qual, info = fields[0], fields[1], fields[3], fields[4], fields[5], fields[7]
                variants.append((chrom, pos, ref, alt, qual, info))

        with open(output_report, "w") as report:
            report.write("Cancer Variant Calling Pipeline - Final Report\n")
            report.write("=" * 50 + "\n\n")
            report.write(f"Total variants found: {len(variants)}\n\n")

            for v in variants:
                chrom, pos, ref, alt, qual, info = v
                report.write(f"Chromosome: {chrom}\n")
                report.write(f"Position: {pos}\n")
                report.write(f"Reference: {ref}\n")
                report.write(f"Alternate: {alt}\n")
                report.write(f"Quality: {qual}\n")
                report.write(f"Info: {info}\n")
                report.write("-" * 50 + "\n")

        print(f"Report generation complete: {output_report}")
        return True
    except Exception as e:
        print(f"Report generation failed: {e}")
        return False


if __name__ == "__main__":
    generate_report(
        input_vcf="results/annotation/annotated.vcf",
        output_report="results/report/final_report.txt"
    )
