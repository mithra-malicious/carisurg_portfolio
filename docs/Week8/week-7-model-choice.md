# Decision Journal — Week 7 Model Choice

**Date:** 2026-07-21
**Decision owner:** Mithra Ramoutar

## Context

- The Week 6 baseline (logistic regression) passed Dr. Reyes' review, but
  the ED Board and Martina Griffith (Clinical IT) asked whether a more
  complex model is worth its extra cost — in accuracy, compute, and
  explainability.
- Recall on ESI 1 was already established in Week 6 as the primary
  clinical metric, so any new model has to be judged against that number
  specifically, not against overall accuracy.

## Alternatives considered

- **Random Forest** (untuned and hyperparameter-tuned via
  `RandomizedSearchCV`) — expected to be a strong, moderately
  interpretable option per the literature; in practice it underperformed
  the baseline on every quality metric, including 0% recall on ESI 1
  untuned.
- **Small MLP** (neural network) — flexible, but per the tutorial's own
  guidance, rarely beats tree models on tabular clinical data and is hard
  to explain; confirmed here — no better than the baseline on macro F1
  and no better on ESI 1 recall.
- **Gradient Boosting** — the only model that improved on ESI 1 recall
  (0.313 vs. baseline's 0.250), though at a cost in accuracy, precision,
  and explainability.

## Decision

Carry Gradient Boosting into Phase 3 piloting, paired with mandatory SHAP
explanations per prediction, while keeping the Week 6 logistic regression
baseline as a documented fallback.

## Reasoning

- Gradient Boosting is the only tested model that improves the metric we
  already told the ED Board matters most — recall on ESI 1 — rather than
  trading it away for a better-looking aggregate number.
- Its inference cost (0.009 ms/prediction) is negligible regardless of
  which model is chosen, so compute cost does not argue against it the
  way it might for a larger/heavier model.
- Explainability is a real cost, not a free pass — SHAP is being adopted
  as a permanent operational requirement alongside the model, not treated
  as optional polish.

## Things I do not yet know

- Whether the ESI 1 recall gain (one additional patient caught, out of 16
  in the test set) holds up under cross-validation or a larger sample —
  the current result rests on a very small absolute count and could
  easily be noise.
- How this recommendation changes once validated against real Mercer
  General data rather than the US academic-hospital benchmark dataset,
  per the standing caveat from the Week 5 memo.
