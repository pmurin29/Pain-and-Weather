# Climate-epidemiology analysis: chronic pain & weather

This repository contains analysis code for linking global chronic pain burden to
long-term climate variables (temperature, sea-level pressure, specific humidity)
using country-level mixed-effects and residual analyses.

The code is structured to be **transparent, modular, and manuscript-ready**.

## Repository structure

```text
climate-epi-analysis/
├── README.md
├── environment.yml
├── LICENSE
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── ne_110m_admin_0_countries.shp
│   │   ├── air.mon.mean.nc
│   │   ├── slp.mon.mean.nc
│   │   ├── shum.mon.mean.nc
│   │   └── complete_dataset_HAQ_GDP.csv
│   └── processed/
│       └── complete_dataset_with_weather.csv
│
├── src/
│   ├── __init__.py
│   ├── load_shapes.py
│   ├── load_weather.py
│   ├── merge_data.py
│   ├── models.py
│   └── utils.py
│
├── scripts/
│   ├── 01_process_weather.py
│   ├── 02_merge_all_data.py
│   ├── 03_run_mixed_models.py
│   └── 04_run_residual_analysis.py
│
└── results/
    ├── model_summaries/
    └── residual_results/
```

## Data inputs

Place the following files in `data/raw/` (not included in the repository):

- `ne_110m_admin_0_countries.shp` and associated files (Natural Earth admin-0 countries)
- `air.mon.mean.nc` (NCEP/NCAR reanalysis monthly air temperature)
- `slp.mon.mean.nc` (NCEP/NCAR reanalysis monthly sea-level pressure)
- `shum.mon.mean.nc` (NCEP/NCAR reanalysis monthly specific humidity)
- `complete_dataset_HAQ_GDP.csv` (epidemiologic dataset with columns such as:
  `year`, `location`, `sex`, `age`, `cause`, `metric`, `val`, `upper`, `lower`,
  `iso_a3`, `population`, `season`, `GDP_per_capita`, `HAQ_index`)

## Quickstart

1. Create and activate the conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate climate-epi-analysis
   ```

2. Run the processing pipeline stepwise:

   ```bash
   # 1. Extract country centroids & compute seasonal weather
   python scripts/01_process_weather.py

   # 2. Merge weather with epidemiologic data
   python scripts/02_merge_all_data.py

   # 3. Fit mixed-effects models for each outcome and weather variable
   python scripts/03_run_mixed_models.py

   # 4. Run residual analyses (GDP/HAQ-adjusted) for each outcome & weather variable
   python scripts/04_run_residual_analysis.py
   ```

The main output dataset used in the manuscript is:

- `data/processed/complete_dataset_with_weather.csv`

Model summaries and residual analyses are written to:

- `results/model_summaries/`
- `results/residual_results/`

## Reproducibility

- All analyses are implemented in plain Python using `pandas`, `xarray`, and
  `statsmodels`.
- Mixed-effects models use `MixedLM` with random intercepts for country (`iso_a3`).
- Residual analyses first regress outcome rates on GDP and HAQ, then regress
  residuals on each weather variable.

## Citation

If you use this code, please cite the associated manuscript:

> Murin P, *et al.* [Title TBD]. Journal, Year.
