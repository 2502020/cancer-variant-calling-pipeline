import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineConfig:
    input_dir: Path
    output_dir: Path
    reference: Path
    quality_threshold: int = 30

    def validate(self) -> None:
        """Validate the pipeline configuration."""

        if not self.input_dir.exists():
            raise FileNotFoundError(
                f"Input directory not found: {self.input_dir}"
            )

        if not self.reference.exists():
            raise FileNotFoundError(
                f"Reference genome not found: {self.reference}"
            )

        if self.quality_threshold < 0:
            raise ValueError(
                "Quality threshold cannot be negative."
            )


def load_config(config_file: str = "config.json") -> PipelineConfig:
    """Load pipeline configuration from a JSON file."""

    with open(config_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    return PipelineConfig(
        input_dir=Path(data["input_dir"]),
        output_dir=Path(data["output_dir"]),
        reference=Path(data["reference"]),
        quality_threshold=data.get("quality_threshold", 30),
    )