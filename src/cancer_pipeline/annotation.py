import os

def annotate_variants(input_vcf: str, output_vcf: str = "results/annotation/annotated.vcf") -> bool:
    """
    Add simple annotation info to each variant (simplified stand-in for VEP).
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
                chrom, pos, ref, alt = fields[0], fields[1], fields[3], fields[4]

                annotation = f"SNV_{ref}>{alt}_at_{chrom}:{pos}"
                fields[7] += f";ANNOTATION={annotation}"

                outfile.write("\t".join(fields) + "\n")

        print(f"Annotation complete: {output_vcf}")
        return True
    except Exception as e:
        print(f"Annotation failed: {e}")
        return False


if __name__ == "__main__":
    annotate_variants(
        input_vcf="results/filtering/filtered.vcf",
        output_vcf="results/annotation/annotated.vcf"
    )
