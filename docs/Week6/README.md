Week 6 — Baseline Triage Models

Two baseline classifiers trained on the Yale EMLC triage dataset to predict ESI level (1–5):
a logistic regression and a decision tree (max_depth=5), benchmarked against a stratified
dummy classifier.


Dataset: yaleemmlc_admissionprediction_triage.csv (55,121 encounters, 226 columns)
Split: 80/20 train/test, stratified on esi, random_state=42
Excluded from all model inputs: disposition, previousdispo (post-visit leakage
columns), Unnamed: 0 (row index, no clinical content)
Primary metric: recall on ESI 1 — not accuracy — because ESI 1 is 0.1% of the data and
a model can score well over 90% accuracy while missing every critical patient


ModelAccuracyMacro F1Recall (ESI 1)Dummy (baseline)0.3750.2040.000Logistic Regression0.6670.4920.250Decision Tree0.5560.2160.000

Notebooks: notebooks/Week6_Tutorial2_Implement_LR_and_DT.ipynb (training) · notebooks/Week6_Tutorial3_Model_Evaluation.ipynb (evaluation)
Full report: docs/week-6-baseline.md
