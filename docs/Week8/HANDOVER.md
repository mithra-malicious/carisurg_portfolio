# Handover — CariSurg Triage Model

**The new-hire Monday test:** could someone who has never met you clone
this repo, read this page, and run the model by end of day — without
asking you a single question? This document is written to pass that
test.

## 1. Project summary

This project builds an explainable AI-assisted triage support tool that
predicts Emergency Severity Index (ESI 1–5) from triage-time vitals and
chief-complaint flags, for the CariSurg MedTech Pathways pilot at Mercer
General Hospital. It is intended to flag under-triage risk while keeping
nurses accountable for the final triage decision — not to replace their
judgement.

## 2. Final model decision

We ship **Gradient Boosting** by default for its ESI-1 recall gain over
the baseline (0.313 vs. 0.250) at negligible inference cost, paired with
mandatory SHAP explanations per prediction; the Week 6 logistic
regression baseline is kept pinned as a documented fallback if SHAP
integration proves too costly for IT Governance sign-off. Full reasoning
and the comparison table: `docs/model-selection.md`.

## 3. How to run

```bash
git clone <repo-url>
cd carisurg-triage
pip install -r requirements.txt

python scripts/train.py --config config.yaml
```

Requires Python 3.10+, git and pip pre-installed. Runs on macOS or Linux.
To evaluate a different pinned model (e.g. the fallback), pass
`--model logistic_regression`.

## 4. Where the data lives

Raw data path is set in `config.yaml` (`data.raw_path`,
`data/yaleemmlc_admissionprediction_triage.csv`). The data directory is
**git-ignored** — it is not committed to this repo. Access is restricted
to the CariSurg research team named in Section 6; the dataset must not be
redistributed. De-identified does **not** mean ungoverned: treat it as
governed patient data at all times.

## 5. Known limitations

- **Single-site benchmark data.** All performance figures are from the
  US academic-hospital Yale EMLC dataset, not Mercer General — local
  validation has not yet been done, and a distribution shift is likely.
- **ESI-1 recall is still modest** (0.313) and rests on a small absolute
  count (16 ESI-1 patients in the test set). This tool is built to
  support the triage nurse's decision, not replace it.
- **Demographics (age, gender, ethnicity, race, etc.) are excluded from
  the model by design.** Testing showed no meaningful accuracy gain from
  including them, so there is no accuracy case for adding
  fairness-sensitive columns back in.

## 6. Who to ask

| Area | Contact |
|---|---|
| Model / methodology questions | Dr. Marcus Reyes |
| Data access / governance | Martina Griffith (Clinical IT Lead) |
| Clinical questions | Dr. L. De Freitas |
