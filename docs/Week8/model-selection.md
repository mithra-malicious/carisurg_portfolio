# Model Selection — Audit Trail

One row per model trained across Weeks 6–7, on the same 55,121-encounter
Yale EMLC dataset and the same 80/20 stratified split (`random_state=42`),
so every row below is apples-to-apples. `disposition`, `previousdispo`,
and the row-index column are excluded as leakage in every run.

| Model | Key hyperparameters | Accuracy | Macro F1 | Recall ESI 1 | Train time | Infer time/pred | Explainability |
|---|---|---|---|---|---|---|---|
| Logistic Regression (baseline) | `max_iter=1000` | 0.667 | 0.492 | 0.250 | 2.88 s | 0.003 ms | High |
| Random Forest (untuned) | `n_estimators=300, class_weight=balanced` | 0.639 | 0.389 | 0.000 | 25.88 s | 0.093 ms | Medium |
| **Gradient Boosting** ★ | `max_depth=6, learning_rate=0.1, max_iter=300, class_weight=balanced` | 0.550 | 0.416 | **0.313** | 10.68 s | 0.009 ms | Low |
| Small MLP | `hidden_layer_sizes=(64,32), alpha=1e-3` | 0.641 | 0.485 | 0.250 | 86.15 s | 0.011 ms | Low |

★ = winner, pinned in `config.yaml` as `final_model: gradient_boosting`.

## Decision

**Carry Gradient Boosting into Phase 3 piloting**, paired with mandatory
SHAP explanations per prediction, while keeping the Week 6 logistic
regression baseline pinned in `config.yaml` (`fallback_model`) as a
documented fallback.

**Why:** Gradient Boosting is the only tested model that improves recall
on ESI 1 — the metric already established as clinically primary — over
the baseline (0.313 vs. 0.250: one additional caught patient out of 16 in
the test set). Its inference cost (0.009 ms/prediction) is negligible
regardless of which model is chosen, so compute is not an argument
against it. It is not the best model by most axes — it is the most
defensible trade given what the ED Board asked to optimise for.

**Full reasoning:** see the Week 7 decision journal and cost-benefit memo
(`docs/week-7-model-choice.md`, `docs/week-7-cost-benefit.md`) for the
three arguments for and against, the sample-size caveats (only 16 ESI 1
patients in the test set; 77 in the full dataset), and the demographics
fairness check (one-hot encoding ethnicity/race gave no meaningful macro
F1 change — 0.387 vs. 0.389 — so they stay excluded).

## Known caveats on these numbers

- All figures above are a US academic-hospital benchmark (Yale EMLC), not
  yet validated against Mercer General data.
- Random Forest and the tuned-forest search were run with a reduced tree
  count/search budget on a single-core environment; a full re-run at the
  assignment's recommended settings (300 trees, 8-iteration/3-fold search)
  is planned before Phase 3 sign-off.
- The ESI-1 recall gain is built on a difference of one patient (5 vs. 4
  of 16) and should be treated as directional until confirmed under
  cross-validation or a larger sample.
