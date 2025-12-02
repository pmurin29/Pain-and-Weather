import os
from typing import Dict, Any

import pandas as pd
import statsmodels.formula.api as smf

WEATHER_VARS = {
    "Temperature (C)": "air_C",
    "Sea-level pressure (hPa)": "slp_hPa",
    "Specific humidity (kg/kg)": "shum_kgkg",
}

def run_mixed_models(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Fit mixed-effects models by cause and weather variable.

    Uses the formula:
        val ~ C(season) + weather + GDP_per_capita + HAQ_index
    with a random intercept for iso_a3.
    """
    results: Dict[str, Dict[str, Any]] = {}
    conditions = df["cause"].unique()

    for label, var in WEATHER_VARS.items():
        results[label] = {}
        for cause in conditions:
            df_c = df[df["cause"] == cause].dropna(
                subset=[var, "GDP_per_capita", "HAQ_index"]
            )
            if df_c.empty:
                continue

            formula = f"val ~ C(season) + {var} + GDP_per_capita + HAQ_index"
            model = smf.mixedlm(formula, df_c, groups=df_c["iso_a3"], missing="drop")
            res = model.fit(reml=True)

            results[label][cause] = res
    return results

def run_residual_analysis(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Two-step residual analysis by cause and weather variable.

    Step 1: val ~ GDP_per_capita + HAQ_index
    Step 2: residuals ~ weather
    """
    output: Dict[str, Dict[str, Any]] = {}
    conditions = df["cause"].unique()

    for label, var in WEATHER_VARS.items():
        output[label] = {}
        for cause in conditions:
            df_c = df[df["cause"] == cause].dropna(
                subset=[var, "GDP_per_capita", "HAQ_index"]
            )
            if df_c.empty:
                continue

            base = smf.ols("val ~ GDP_per_capita + HAQ_index", data=df_c).fit()
            df_c = df_c.copy()
            df_c["residuals"] = base.resid

            weather = smf.ols(f"residuals ~ {var}", data=df_c).fit()

            output[label][cause] = {"base": base, "weather": weather}
    return output

def save_model_summaries(results: Dict[str, Dict[str, Any]], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for label, conds in results.items():
        for cause, res in conds.items():
            fname = f"{label.replace(' ', '_')}_{cause.replace(' ', '_')}.txt"
            path = os.path.join(out_dir, fname)
            with open(path, "w") as f:
                f.write(str(res.summary()))

def save_residual_summaries(results: Dict[str, Dict[str, Any]], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for label, conds in results.items():
        for cause, res_dict in conds.items():
            base = res_dict["base"]
            weather = res_dict["weather"]
            fname = f"residual_{label.replace(' ', '_')}_{cause.replace(' ', '_')}.txt"
            path = os.path.join(out_dir, fname)
            with open(path, "w") as f:
                f.write("Base model: val ~ GDP_per_capita + HAQ_index\n\n")
                f.write(str(base.summary()))
                f.write("\n\nWeather on residuals:\n\n")
                f.write(str(weather.summary()))
