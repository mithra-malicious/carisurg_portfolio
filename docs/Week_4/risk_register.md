# Risk Register — AI-Assisted Triage Support Tool
**Project:** AI-Assisted Triage Support Tool for High-Risk Patient Identification in the ED  
**Author:** Mithra Ramoutar  
**Week:** 4 — Ethics, Safety & Risk Awareness  
**Status:** Draft (Interim)

---

## Risk Categories
- **AI-Technical** — risks arising from model design, training data, or algorithmic behaviour
- **Operational** — risks arising from clinical workflow, staffing, or system integration
- **Ethical** — risks arising from accountability, consent, and clinician decision-making
- **Equity** — risks arising from unequal performance across patient demographic groups

---

## Risk Register

| # | Risk Name | Category | Likelihood | Impact | Mitigation | Signal of Success |
|---|-----------|----------|------------|--------|------------|-------------------|
| 1 | Demographic bias in training data | AI-Technical | High | High | Audit training data for demographic distribution; apply re-weighting or stratified sampling to correct imbalances before deployment. | Sensitivity and specificity are statistically equivalent across race, ethnicity, language, and age groups in pilot evaluation. |
| 2 | Distribution shift — model trained on non-Caribbean data | AI-Technical | High | High | Fine-tune model on locally sourced Mercer ED data before deployment; retrain quarterly as patient demographics shift. | Model performance on local validation set meets or exceeds published benchmarks within one standard deviation. |
| 3 | NLP degradation on abbreviated free-text triage notes | AI-Technical | Medium | High | Calibrate NLP component on a representative sample of real Mercer triage notes, including abbreviated and colloquial entries, prior to go-live. | NLP classification accuracy on locally sourced notes is within 5% of accuracy on clean clinical corpus. |
| 4 | Alert fatigue leading to clinician disengagement | Operational | High | High | Set high-confidence alert threshold (>0.85 probability); target fewer than 5 alerts per shift; conduct pre-launch calibration with Sr. Patrice Alleyne. | Alert override rate remains below 30% at four weeks post-deployment; nurses report tool as helpful on weekly usability survey. |
| 5 | EHR data lag causing stale inputs at point of alert | Operational | High | Medium | Design tool to operate on data available at triage card completion, not EHR confirmation; display data-age indicator alongside each alert. | Fewer than 10% of alerts are triggered on inputs more than 15 minutes old during pilot monitoring. |
| 6 | Automation bias — nurses deferring to AI over clinical judgement | Ethical | Medium | High | Train all triage nurses on AI limitations before go-live; design UI to show alert as advisory not directive; log all override decisions for audit. | Nurses correctly override the tool in at least 80% of injected test scenarios where the AI recommendation is deliberately incorrect. |
| 7 | Lack of informed patient consent for AI-assisted triage | Ethical | Medium | Medium | Display a visible notice in the triage waiting area explaining that AI tools support — not replace — nurse decisions; obtain ethics board clearance before pilot launch. | Ethics board approval obtained; patient complaint rate related to AI use remains at zero during pilot. |
| 8 | Underperformance on paediatric and elderly patients | Equity | Medium | High | Stratify pilot evaluation data by age group; if performance gap exceeds 5% between adult and paediatric/elderly cohorts, restrict tool use to adult patients pending retraining. | Sensitivity gap between adult and paediatric/elderly cohorts is less than 5% in pilot evaluation report. |

---

## Real-World Harm Case Study

**Incident:** Epic Sepsis Model — University of Michigan Health System (2021)

An independent audit of the Epic Sepsis Model (ESM), published in *JAMA Internal Medicine* by Wong et al. (2021), found that the algorithm had a positive predictive value of just 12.8% and missed 33.4% of patients who did develop sepsis — despite being in active clinical use across multiple US hospital systems.

**Root causes identified:**
- Training-deployment distribution shift: model trained on a single institution's data, deployed without independent validation across different populations
- Opaque validation reporting: source code, training data, and full performance statistics were not published
- Automation bias: alert design made clinical deferral feel like inaction
- No signal-of-success monitoring: no pre-defined thresholds to trigger review or suspension

**Relevance to this pilot:** Distribution shift and automation bias are both rated High/High in this register. The ESM case directly informs three design decisions: local validation before deployment, continuous performance monitoring with pre-defined review thresholds, and an alert UI that makes override cognitively easy.

**Source:** Wong, A., et al. (2021). External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. *JAMA Internal Medicine, 181*(8), 1065–1070. https://doi.org/10.1001/jamainternmed.2021.2626

---
