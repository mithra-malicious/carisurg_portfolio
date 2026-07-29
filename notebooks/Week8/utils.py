"""
src/utils.py — shared helpers
"""

from __future__ import annotations

import yaml
from sklearn.model_selection import train_test_split


def load_config(path: str) -> dict:
    """Load config.yaml into a plain dict."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def make_split(X, y, seed: int, test_size: float = 0.2):
    """Reproduce the standing Week 6 split: 80/20, stratified, fixed seed.

    Same random_state everywhere -> identical test patients every run,
    which is what lets docs/model-selection.md compare models fairly.
    """
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=seed)
