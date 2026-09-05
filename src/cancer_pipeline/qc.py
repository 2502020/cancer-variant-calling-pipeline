import subprocess
import os

def run_fastqc(input_file: str, output_dir: str = "results/fastqc") -> bool:
    """
    Run FastQC on a given FASTQ file using Python's subprocess module.
    Returns True if successful, False otherwise.
    """
    os.makedirs(output_dir, exist_ok=True)

    command = ["fastqc", input_file, "-o", output_dir]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FastQC failed: {e.stderr}")
        return False


if __name__ == "__main__":
    # Quick manual test
    run_fastqc("data/input/sample_test.fastq")
