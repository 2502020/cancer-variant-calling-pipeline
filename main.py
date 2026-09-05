from src.cancer_pipeline.pipeline import run_pipeline

if __name__ == "__main__":
    success = run_pipeline("config.json")
    if success:
        print("\nPipeline completed successfully! Check results/report/final_report.txt")
    else:
        print("\nPipeline failed. Check logs/pipeline.log for details.")
