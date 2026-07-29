"""
tests/test_pipeline.py

Two sanity checks (Week 8, Task 4). These do not prove the pipeline is
"correct" — they prove it fails LOUDLY the moment a change would
silently corrupt the data or break training, instead of quietly
degrading the model.

Run with:
    pytest tests/test_pipeline.py -v
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data import clean
from src.features import add_clinical_features, select_features
from src.model import build_model


def _tiny_raw_frame(n=60):
    """A small synthetic frame shaped like the real raw CSV, so the
    smoke test does not depend on the real (governed) patient data
    being present on disk."""
    import numpy as np

    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "esi": rng.integers(1, 6, size=n),
        "triage_vital_hr": rng.normal(85, 15, size=n),
        "triage_vital_sbp": rng.normal(120, 15, size=n),
        "triage_vital_dbp": rng.normal(75, 10, size=n),
        "triage_vital_rr": rng.normal(18, 4, size=n),
        "triage_vital_o2": rng.normal(97, 3, size=n),
        "triage_vital_temp": rng.normal(98.6, 1.0, size=n),
        "triage_glucose": rng.normal(100, 20, size=n),
        "age": rng.integers(1, 95, size=n),
        "gender": rng.choice(["male", "female", "M", "F"], size=n),
        "ethnicity": rng.choice(["A", "B"], size=n),
        "race": rng.choice(["X", "Y"], size=n),
        "disposition": rng.choice(["admit", "discharge"], size=n),
        "previousdispo": rng.choice(["admit", "discharge"], size=n),
        "dep_name": "ED",
        "arrivalmode": "walk-in",
        "arrivalmonth": 1,
        "arrivalday": 1,
        "arrivalhour_bin": 1,
    })


def test_clean_produces_valid_schema():
    """After cleaning, is the data the shape the model expects?"""
    raw = _tiny_raw_frame()
    df = clean(raw)
    assert df["esi"].isin([1, 2, 3, 4, 5]).all()          # only valid labels
    assert df["triage_vital_hr"].isna().sum() == 0          # no gaps
    assert set(df["gender"].unique()) <= {0, 1}             # encoded
    assert len(df) > 0                                       # not empty


def test_smoke_train_predict():
    """Does the whole pipeline run on a tiny slice without crashing?"""
    raw = _tiny_raw_frame(60)
    df = clean(raw)
    X, y = select_features(df)
    X = add_clinical_features(X)

    # Not enough rows/classes for a stratified split at this size, so
    # just fit and predict on the same tiny slice -- this test checks
    # the pipeline *runs end to end*, not that it's accurate.
    model = build_model("gradient_boosting", {"max_iter": 20, "max_depth": 3}, seed=42)
    model.fit(X, y)
    preds = model.predict(X)
    assert len(preds) == len(y)
