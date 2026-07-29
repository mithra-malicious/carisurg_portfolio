# Week 7 — Cost-Benefit Memo: Model Selection for Phase 3

**To:** Dr. L. De Freitas, Mercer General ED Board, Martina Griffith (Clinical IT Lead)
**From:** Mithra Ramoutar, Clinical AI Research Trainee
**Re:** Is a more sophisticated model worth the extra complexity for Phase 3?

## Verdict

Recommend Gradient Boosting for Phase 3, on the strength of its recall
gain on ESI 1 patients — the metric established as clinically primary —
on the condition that every prediction is paired with a SHAP explanation
to meet interpretability and audit requirements. None of the other
complex models tested (Random Forest, tuned or untuned; a small neural
network) beat the Week 6 baseline on any axis that matters clinically.

## Recap: dataset and method

Still predicting ESI (1–5) from triage-time vitals and chief-complaint
flags only, using the same 55,121-encounter Yale EMLC dataset and the
same 80/20 stratified split (`random_state=42`) as Week 6, so every
comparison below is apples-to-apples. `disposition`, `previousdispo`, and
the row-index column remain excluded as leakage. This week engineered
three additional clinical red-flag features (tachypnoea, hypoxia, fever,
and a combined red-flag count) and tested three more complex models
against the Week 6 logistic regression baseline: a Random Forest, a
Gradient Boosting model, and a small neural network (MLP).

## Benchmark table

| Model | Accuracy | Macro F1 | Recall ESI 1 | Train time | Infer time/pred | Explainability |
|---|---|---|---|---|---|---|
| Baseline (LogReg) | 0.667 | 0.492 | 0.250 | 2.88 s | 0.003 ms | High |
| Random Forest | 0.639 | 0.389 | 0.000 | 25.88 s | 0.093 ms | Medium |
| Gradient Boosting | 0.550 | 0.416 | 0.313 | 10.68 s | 0.009 ms | Low |
| Small MLP | 0.641 | 0.485 | 0.250 | 86.15 s | 0.011 ms | Low |

(Full table with precision/recall macro figures, the tuned-forest result,
and the demographics-inclusion test are in `docs/week-7-benchmark.md`.)

## Three arguments for Gradient Boosting

1. **It is the only model that improves on the metric we said mattered
   most.** Week 6 established recall on ESI 1 as the primary metric,
   specifically because a missed critical patient is the costliest error
   in this system. Gradient Boosting catches 5 of 16 ESI 1 test patients
   versus the baseline's 4 of 16 — a real, if modest, improvement on
   exactly that number.
2. **Its inference cost is trivially small.** At 0.009 ms per prediction,
   it is well within any real-time triage workflow — Martina Griffith's
   "paid on every prediction, forever" cost is a non-issue here regardless
   of which model wins.
3. **Its macro-recall is also the best of the four (0.547)**, meaning it
   is more willing to flag urgency broadly, not just for ESI 1
   specifically — useful if the ED Board's real concern is under-triage
   in general, not just the rarest class.

## Three arguments against Gradient Boosting

1. **It is the least accurate and least precise model tested.** Accuracy
   (0.550) and precision (0.410) are both the worst of the four — it
   generates meaningfully more false alarms than the baseline, which has
   its own operational cost (alarm fatigue, wasted resources on
   over-triaged patients).
2. **It is the hardest to explain.** Per the Week 7 tutorial's own
   interpretability ranking, gradient boosting requires SHAP to explain
   even a single prediction — Dr. Reyes cannot trace a decision by hand
   the way he could with the baseline's weights or a single tree.
   Adopting it means adopting SHAP as a permanent operational dependency,
   not a one-time analysis step.
3. **The absolute numbers behind this recommendation are small.** Only 16
   ESI 1 patients exist in the test set; the entire "improvement" is one
   additional patient caught (5 vs. 4). A result built on a difference of
   one patient is not yet a result we should treat as settled — it needs
   to hold up under cross-validation and, eventually, local Mercer data,
   before it justifies a production decision.

## Risks and unknowns

- **Sample size.** With only 77 ESI 1 encounters in the entire
  55,121-row dataset, every ESI 1 recall figure in this memo is built on
  single-digit counts of test patients. These numbers should be treated
  as directional, not final, until validated with cross-validation and
  (eventually) a larger or locally-collected sample.
- **Demographics do not help.** One-hot encoded ethnicity and race were
  tested against the Random Forest and found no meaningful change in
  macro F1 (0.387 vs. 0.389 without them) — meaning there is no accuracy
  case for including fairness-sensitive columns in any model going
  forward, and we recommend they stay excluded regardless of which model
  is chosen.
- **Compute environment for these figures.** Random Forest and the
  tuned-forest search were run with a reduced tree count and search
  budget for this memo's benchmark run, due to the single-core
  environment used to produce it; a full re-run with the assignment's
  recommended settings (300 trees, 8-iteration/3-fold search) is planned
  before Phase 3 sign-off, though the gap between the baseline and the
  other models is wide enough that this is unlikely to change the
  recommendation.
- **No local validation yet.** As flagged since Week 5, every figure here
  is a US academic-hospital benchmark, not a guarantee of Mercer General
  performance.

## Recommendation

Carry Gradient Boosting into Phase 3 piloting, paired with SHAP
explanations at the point of each prediction, specifically because it is
the only model tested that improves recall on the class we have already
told the ED Board is our top clinical priority. This is not "the best
model" by most axes — it is the most defensible trade given what we are
optimising for. The baseline remains a credible fallback if SHAP
integration proves too costly for Martina Griffith's IT Governance
requirements; it should not be discarded.
