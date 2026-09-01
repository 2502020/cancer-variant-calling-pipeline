from pathlib import Path

from src.cancer_pipeline.config import PipelineConfig


def validate_input(config: PipelineConfig) -> None:
    """Validate required pipeline inputs and directories."""

    if not config.input_dir.exists():
        raise FileNotFoundError(
            f"Input directory does not exist: {config.input_dir}"
        )

    if not config.reference.exists():
        raise FileNotFoundError(
            f"Reference genome does not exist: {config.reference}"
        )

    if not config.output_dir.exists():
        config.output_dir.mkdir(parents=True, exist_ok=True)

    print("Input validation completed successfully.")