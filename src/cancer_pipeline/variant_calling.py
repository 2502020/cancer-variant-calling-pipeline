import subprocess
import os

def call_variants(reference: str, input_bam: str, output_vcf: str = "results/variants/output.vcf") -> bool:
    """
    Call variants from a sorted BAM file against a reference genome using bcftools.
    Returns True if successful, False otherwise.
    """
    os.makedirs(os.path.dirname(output_vcf), exist_ok=True)

    try:
        mpileup_command = ["bcftools", "mpileup", "-B", "-Q", "0", "-f", reference, input_bam]
        call_command = ["bcftools", "call", "-mv", "-o", output_vcf]

        mpileup_process = subprocess.Popen(mpileup_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        call_process = subprocess.run(
            call_command,
            stdin=mpileup_process.stdout,
            capture_output=True,
            text=True,
            check=True
        )
        mpileup_process.stdout.close()

        print(f"Variant calling complete: {output_vcf}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Variant calling failed: {e.stderr}")
        return False


if __name__ == "__main__":
    call_variants(
        reference="data/reference/reference.fa",
        input_bam="results/alignment/mutant_sorted.bam",
        output_vcf="results/variants/mutant.vcf"
    )
