import subprocess
import os

def run_alignment(reference: str, input_fastq: str, output_sam: str = "results/alignment/output.sam") -> bool:
    """
    Align a FASTQ file against a reference genome using BWA.
    Returns True if successful, False otherwise.
    """
    os.makedirs(os.path.dirname(output_sam), exist_ok=True)

    command = ["bwa", "mem", reference, input_fastq]

    try:
        with open(output_sam, "w") as out_file:
            result = subprocess.run(
                command,
                stdout=out_file,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        print(f"Alignment complete: {output_sam}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"BWA alignment failed: {e.stderr}")
        return False


if __name__ == "__main__":
    run_alignment(
        reference="data/reference/reference.fa",
        input_fastq="data/input/sample_test.fastq",
        output_sam="results/alignment/sample_test.sam"
    )
