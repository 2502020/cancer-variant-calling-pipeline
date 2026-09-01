from src.cancer_pipeline.config import load_config
from src.cancer_pipeline.validator import validate_input


def main():
    print("Cancer Variant Calling and Annotation Pipeline")
    print("=" * 50)

    config = load_config()

    print(f"Input directory: {config.input_dir}")
    print(f"Output directory: {config.output_dir}")
    print(f"Reference genome: {config.reference}")
    print(f"Quality threshold: {config.quality_threshold}")

    print("\nValidating pipeline inputs...")

    try:
        validate_input(config)
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}")
        return 1

    print("\nPipeline environment is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())