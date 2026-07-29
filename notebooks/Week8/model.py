"""
src/model.py — train & evaluate

Builds a model from config (logistic_regression / random_forest /
gradient_boosting) and scores it on the axes the Week 7 cost-benefit
memo used: accuracy, macro-F1, ESI-1 recall, train time, and
inference time.
"""

from __future__ import annotations

import time

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ESI_1 = 1


def build_model(name: str, params: dict, seed: int):
    """Construct a model (or scaled pipeline) from a config block.

    Parameters
    ----------
    name : str
        One of "logistic_regression", "random_forest", "gradient_boosting".
    params : dict
        Hyperparameters from config.yaml for this model.
    seed : int
        random_state, applied on top of anything already in params.
    """
    params = dict(params or {})
    params.setdefault("random_state", seed)

    if name == "logistic_regression":
        return make_pipeline(StandardScaler(), LogisticRegression(**params))

    if name == "random_forest":
        return RandomForestClassifier(**params)

    if name == "gradient_boosting":
        return HistGradientBoostingClassifier(**params)

    if name == "mlp":
        from sklearn.neural_network import MLPClassifier

        return make_pipeline(StandardScaler(), MLPClassifier(**params))

    raise ValueError(f"Unknown model name '{name}'. Expected one of: "
                      "logistic_regression, random_forest, gradient_boosting, mlp.")


def fit_timed(model, X_train, y_train):
    """Fit a model and return (model, train_time_seconds)."""
    start = time.perf_counter()
    model.fit(X_train, y_train)
    return model, time.perf_counter() - start


def evaluate(model, X, y) -> dict:
    """Score a fitted model on the six-axis benchmark used in docs/model-selection.md.

    Returns a dict with accuracy, macro precision/recall/F1, ESI-1
    recall specifically, and per-prediction inference time in ms.
    """
    start = time.perf_counter()
    preds = model.predict(X)
    elapsed = time.perf_counter() - start
    infer_ms_per_pred = (elapsed / len(X)) * 1000 if len(X) else float("nan")

    esi1_mask = (y == ESI_1)
    if esi1_mask.sum() > 0:
        recall_esi1 = recall_score(y == ESI_1, preds == ESI_1, pos_label=True, zero_division=0)
    else:
        recall_esi1 = float("nan")

    return {
        "accuracy": accuracy_score(y, preds),
        "precision_macro": precision_score(y, preds, average="macro", zero_division=0),
        "recall_macro": recall_score(y, preds, average="macro", zero_division=0),
        "f1_macro": f1_score(y, preds, average="macro", zero_division=0),
        "recall_esi1": recall_esi1,
        "infer_ms_per_pred": infer_ms_per_pred,
    }
