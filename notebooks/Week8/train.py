"""
scripts/train.py — the one command that runs the whole pipeline.

    python scripts/train.py --config config.yaml
    python scripts/train.py --config config.yaml --model gradient_boosting

No manual cell-running, no hidden state: config.yaml drives everything.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data import clean, load_raw
from src.features import add_clinical_features, select_features
from src.model import build_model, evaluate, fit_timed
from src.utils import load_config, make_split


def parse_args():
    parser = argparse.ArgumentParser(description="Train and evaluate the CariSurg triage model.")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    parser.add_argument(
        "--model",
        default=None,
        help="Override config's final_model (e.g. --model logistic_regression)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)

    model_name = args.model or cfg["final_model"]
    seed = cfg["seed"]

    print(f"[1/5] Loading + cleaning: {cfg['data']['raw_path']}")
    df = clean(load_raw(cfg["data"]["raw_path"]))
    print(f"      -> modelling table: {df.shape[0]} rows x {df.shape[1]} cols")

    print("[2/5] Selecting + engineering features (demographics excluded by default)")
    X, y = select_features(df, target=cfg["data"]["target"])
    X = add_clinical_features(X)
    print(f"      -> {X.shape[1]} features")

    print(f"[3/5] Splitting (seed={seed}, stratified 80/20)")
    X_train, X_test, y_train, y_test = make_split(X, y, seed=seed)
    print(f"      -> train: {X_train.shape[0]} | test: {X_test.shape[0]}")

    print(f"[4/5] Building + training '{model_name}'")
    model = build_model(model_name, cfg["models"][model_name], seed=seed)
    model, train_time = fit_timed(model, X_train, y_train)
    print(f"      -> trained in {train_time:.2f}s")

    print("[5/5] Evaluating on held-out test set")
    metrics = evaluate(model, X_test, y_test)
    print()
    print(f"Model: {model_name}")
    for key, value in metrics.items():
        print(f"  {key:20s}: {value:.4f}" if value == value else f"  {key:20s}: n/a")
    print(f"  {'train_time_s':20s}: {train_time:.4f}")


if __name__ == "__main__":
    main()
