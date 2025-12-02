"""
Step 4: Run residual analyses by weather variable and condition.

1) val ~ GDP_per_capita + HAQ_index
2) residuals ~ weather
"""
import os
import pandas as pd
from src.models import run_residual_analysis, save_residual_summaries

DATA_PROCESSED = "data/processed"
RESULTS_DIR = "results/residual_results"

MERGED_CSV = os.path.join(DATA_PROCESSED, "complete_dataset_with_weather.csv")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    df = pd.read_csv(MERGED_CSV)
    df = df[df["metric"] == "Rate"].copy()

    results = run_residual_analysis(df)
    save_residual_summaries(results, RESULTS_DIR)
    print(f"Saved residual analysis summaries to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
