from pathlib import Path

from src.cancer_pipeline.config import load_config
from src.cancer_pipeline.logger import setup_logger
from src.cancer_pipeline.validator import validate_input
from src.cancer_pipeline.qc import run_fastqc
from src.cancer_pipeline.alignment import run_alignment
from src.cancer_pipeline.bam_processing import process_bam
from src.cancer_pipeline.variant_calling import call_variants
from src.cancer_pipeline.filtering import filter_variants
from src.cancer_pipeline.annotation import annotate_variants
from src.cancer_pipeline.reporting import generate_report


def run_pipeline(config_file: str = "config.json") -> bool:
    """
    Orchestrate the full cancer variant calling pipeline, stage by stage.
    Returns True if all stages completed successfully, False otherwise.
    """
    config = load_config(config_file)
    logger = setup_logger(Path("logs"))

    logger.info("Pipeline started")

    try:
        input_fastq = str(next(config.input_dir.glob("*.fastq")))
        reference = str(config.reference)
    except StopIteration:
        logger.error(f"No FASTQ file found in {config.input_dir}")
        return False

    stages = [
        ("Quality Control", lambda: run_fastqc(input_fastq, str(config.output_dir / "fastqc"))),
        ("Alignment", lambda: run_alignment(reference, input_fastq, str(config.output_dir / "alignment" / "aligned.sam"))),
        ("BAM Processing", lambda: process_bam(str(config.output_dir / "alignment" / "aligned.sam"), str(config.output_dir / "alignment" / "aligned_sorted.bam"))),
        ("Variant Calling", lambda: call_variants(reference, str(config.output_dir / "alignment" / "aligned_sorted.bam"), str(config.output_dir / "variants" / "variants.vcf"))),
        ("Filtering", lambda: filter_variants(str(config.output_dir / "variants" / "variants.vcf"), str(config.output_dir / "filtering" / "filtered.vcf"), config.quality_threshold)),
        ("Annotation", lambda: annotate_variants(str(config.output_dir / "filtering" / "filtered.vcf"), str(config.output_dir / "annotation" / "annotated.vcf"))),
        ("Report Generation", lambda: generate_report(str(config.output_dir / "annotation" / "annotated.vcf"), str(config.output_dir / "report" / "final_report.txt"))),
    ]

    for stage_name, stage_func in stages:
        logger.info(f"Starting stage: {stage_name}")
        success = stage_func()
        if not success:
            logger.error(f"Pipeline failed at stage: {stage_name}")
            return False
        logger.info(f"Completed stage: {stage_name}")

    logger.info("Pipeline completed successfully")
    return True
