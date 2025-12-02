"""
Step 3: Fit mixed-effects models for each chronic pain condition and weather variable.
"""
import os
import pandas as pd
from src.models import run_mixed_models, save_model_summaries

DATA_PROCESSED = "data/processed"
RESULTS_DIR = "results/model_summaries"

MERGED_CSV = os.path.join(DATA_PROCESSED, "complete_dataset_with_weather.csv")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    df = pd.read_csv(MERGED_CSV)
    # Focus on rate metric
    df = df[df["metric"] == "Rate"].copy()

    results = run_mixed_models(df)
    save_model_summaries(results, RESULTS_DIR)
    print(f"Saved mixed model summaries to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
