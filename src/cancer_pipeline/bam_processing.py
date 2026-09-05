import subprocess
import os

def process_bam(input_sam: str, output_bam: str = "results/alignment/output_sorted.bam") -> bool:
    """
    Convert SAM to sorted, indexed BAM using samtools.
    Returns True if successful, False otherwise.
    """
    os.makedirs(os.path.dirname(output_bam), exist_ok=True)

    try:
        # Convert SAM to BAM and sort in one step
        sort_command = ["samtools", "sort", "-o", output_bam, input_sam]
        subprocess.run(sort_command, capture_output=True, text=True, check=True)

        # Index the sorted BAM
        index_command = ["samtools", "index", output_bam]
        subprocess.run(index_command, capture_output=True, text=True, check=True)

        print(f"BAM processing complete: {output_bam}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"BAM processing failed: {e.stderr}")
        return False


if __name__ == "__main__":
    process_bam(
        input_sam="results/alignment/sample_test.sam",
        output_bam="results/alignment/sample_test_sorted.bam"
    )
