"""
src/features.py — engineer & encode

Turns the cleaned modelling table into model-ready X/y: choosing which
columns are fair game, engineering clinical red-flag features, and
(optionally, off by default) encoding demographics.
"""

from __future__ import annotations

import pandas as pd

TARGET = "esi"

DEMOGRAPHICS = [
    "age", "gender", "ethnicity", "race", "lang",
    "religion", "maritalstatus", "employstatus", "insurance_status",
]
ADMIN = ["dep_name", "arrivalmode", "arrivalmonth", "arrivalday", "arrivalhour_bin"]
# Outcomes of the visit — known only AFTER triage. Never model inputs.
LEAKAGE = ["disposition", "previousdispo"]


def select_features(df: pd.DataFrame, target: str = TARGET):
    """Choose columns that are fair game at triage time.

    Excludes leakage (post-triage outcomes), admin/arrival metadata, and
    — by default — demographics (some of which are fairness-sensitive;
    see encode_demographics() to bring them back in deliberately).

    Returns (X, y).
    """
    features = [c for c in df.columns if c != target and c not in LEAKAGE + ADMIN + DEMOGRAPHICS]
    X = df[features].copy()
    y = df[target].copy()
    return X, y


def add_clinical_features(X: pd.DataFrame) -> pd.DataFrame:
    """Add engineered clinical red-flag features (Week 7).

    Built row-by-row from vitals already in X, so it is safe to apply
    to train and test splits independently — no leakage between rows.
    """
    out = X.copy()

    out["shock_index"] = out["triage_vital_hr"] / out["triage_vital_sbp"]
    out["pulse_pressure"] = out["triage_vital_sbp"] - out["triage_vital_dbp"]
    out["spo2_rr_ratio"] = out["triage_vital_o2"] / out["triage_vital_rr"]

    out["is_tachypneic"] = (out["triage_vital_rr"] > 20).astype(int)
    out["is_hypoxic"] = (out["triage_vital_o2"] < 92).astype(int)
    out["is_febrile"] = (out["triage_vital_temp"] >= 100.4).astype(int)

    out["red_flag_count"] = out[["is_tachypneic", "is_hypoxic", "is_febrile"]].sum(axis=1)

    return out


def encode_demographics(X: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode demographics and bolt them onto X — OFF by default.

    Week 7 found no meaningful macro-F1 change from including
    demographics (0.387 vs 0.389 without them), so this is not called
    from the default training path in scripts/train.py. Kept available
    for anyone who needs to re-run that fairness check, aligned by row
    index so it is safe to call on train/test splits separately.
    """
    rows = X.index
    demo_1hot = pd.get_dummies(df.loc[rows, ["ethnicity", "race"]], prefix=["eth", "race"], dtype=int)
    out = pd.concat([X, demo_1hot], axis=1)
    out["age"] = df.loc[rows, "age"]
    out["gender"] = df.loc[rows, "gender"]
    return out
