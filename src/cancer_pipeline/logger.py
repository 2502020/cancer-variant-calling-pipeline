import logging
from pathlib import Path


def setup_logger(log_dir: Path) -> logging.Logger:
    """Create and configure the pipeline logger."""

    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "pipeline.log"

    logger = logging.getLogger("cancer_pipeline")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger