import os

def filter_variants(input_vcf: str, output_vcf: str = "results/filtering/filtered.vcf", min_quality: float = 10.0) -> bool:
    """
    Filter a VCF file, keeping only variants with quality >= min_quality.
    Returns True if successful, False otherwise.
    """
    os.makedirs(os.path.dirname(output_vcf), exist_ok=True)

    try:
        with open(input_vcf, "r") as infile, open(output_vcf, "w") as outfile:
            for line in infile:
                if line.startswith("#"):
                    outfile.write(line)
                    continue

                fields = line.strip().split("\t")
                qual = float(fields[5])

                if qual >= min_quality:
                    outfile.write(line)

        print(f"Filtering complete: {output_vcf}")
        return True
    except Exception as e:
        print(f"Filtering failed: {e}")
        return False


if __name__ == "__main__":
    filter_variants(
        input_vcf="results/variants/mutant.vcf",
        output_vcf="results/filtering/filtered.vcf",
        min_quality=10.0
    )
