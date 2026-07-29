"""
src/data.py — load & clean

Turns the raw Yale EMLC triage CSV into a modelling-ready DataFrame.
This is the Week 5 cleaning logic, extracted from the notebooks as
plain functions so it can be imported, tested, and reused instead of
re-run cell by cell.
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

# Vital-sign columns measured at the front door.
VITALS = [
    "triage_vital_hr",
    "triage_vital_sbp",
    "triage_vital_dbp",
    "triage_vital_rr",
    "triage_vital_o2",
    "triage_vital_temp",
    "triage_glucose",
]

VALID_ESI = {1, 2, 3, 4, 5}


def load_raw(path: str) -> pd.DataFrame:
    """Read the raw triage CSV into a DataFrame.

    Parameters
    ----------
    path : str
        Path to the raw CSV (e.g. ``data/yaleemmlc_admissionprediction_triage.csv``).
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Raw data file not found at '{path}'. Check config.yaml -> data.raw_path, "
            "and confirm the file has been placed in data/ (see docs/HANDOVER.md for "
            "governance status before copying real patient data anywhere)."
        )
    return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Turn the raw triage table into a modelling-ready DataFrame.

    Mirrors the Week 5/7 notebook cleaning cell exactly, so re-running
    this function on the same raw file reproduces the same modelling
    table:
      1. Drop stray index columns pandas may have added.
      2. Coerce vitals to numeric; unparseable values become NaN.
      3. Drop rows with a missing/invalid ESI label (1-5 only).
      4. Blank out physically impossible vitals (temp, o2 out of range).
      5. Encode gender to 0/1.
      6. Impute remaining missing numeric values with the column median.
    """
    out = df.copy()

    # 1) drop stray index columns (e.g. "Unnamed: 0")
    out = out.drop(columns=[c for c in out.columns if c.startswith("Unnamed")], errors="ignore")

    # 2) force vitals to numeric
    for col in VITALS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    # 3) ESI must be 1-5; drop rows that can't teach the model anything
    out["esi"] = pd.to_numeric(out["esi"], errors="coerce")
    out = out[out["esi"].isin(VALID_ESI)].copy()

    # 4) blank out physically impossible vitals
    out.loc[(out["triage_vital_temp"] < 90) | (out["triage_vital_temp"] > 110), "triage_vital_temp"] = np.nan
    out.loc[out["triage_vital_o2"] > 100, "triage_vital_o2"] = np.nan

    # 5) encode gender to 0/1, tolerating odd casing
    out["gender"] = (
        out["gender"].astype(str).str.strip().str.lower().map({"male": 0, "m": 0, "female": 1, "f": 1})
    )

    # 6) impute remaining numeric gaps with the column median
    for col in VITALS + ["age", "gender"]:
        if col in out.columns:
            out[col] = out[col].fillna(out[col].median())

    out["esi"] = out["esi"].astype(int)
    return out
