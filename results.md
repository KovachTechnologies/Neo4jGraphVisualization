# Gravity Model for Identity Resolution: Research Summary and Experimental Results

---

## Overview

This page summarizes a series of experiments evaluating variations of a **gravity model** for identity resolution. The model is inspired by Newton's law of universal gravitation and is used to quantify the affinity or "pull" between customers and stores (or other entities) for matching and resolution purposes.

### Core Gravity Model Formulation

The baseline model is defined as:

**G = (M₁ × M₂) / r²**

Where:
- **M₁** = Total store revenue / "mass" (e.g., total store $)
- **M₂** = Total customer spend at that store
- **r** = Distance or dissimilarity metric (geographic, behavioral, embedding-based, etc.)

The objective of this research program is to systematically vary the formula (exponents, additive/multiplicative terms, hybrid constructions) and measure impact on key performance metrics, with particular attention to F1-score and record-level stability (impact).

**Key Question:** Is the default formulation optimal, or do dataset biases and temporal effects favor it artificially?

---

## Section 1: Comparative Model Performance (F1-Score Analysis)

**Evaluation Date:** 2026-05-18

Five different gravity model formulations (and variations thereof) were implemented and benchmarked. Performance was measured using **F1-score** on a held-out evaluation set.

### Models Evaluated
- Baseline: Classic `G = M1 × M2 / r²`
- Variant A: Modified distance exponent (e.g., `/ r` or `/ r³`)
- Variant B: Log-transformed masses or distance
- Variant C: Multiplicative scaling factors or additional feature terms
- Variant D / Hybrid precursors: Early combinations of gravity + auxiliary signals

### Results

**F1-Score Comparison Across Models**  
*(Attach chart: bar or grouped comparison of F1-scores for all five models + baseline)*

**Primary Finding:**  
The **default model (G = M₁ × M₂ / r²)** achieved the **highest F1-score** among all tested variants.

**Secondary Observation:**  
Several variants underperformed the baseline, sometimes by a meaningful margin.

**Interpretation & Caveat**  
While these results initially suggest the classical gravity formulation is superior, they **may indicate bias in the evaluation dataset**. The data distribution could be inadvertently aligned with the assumptions embedded in the original `M1 × M2 / r²` form (e.g., strong correlation between store revenue, customer spend concentration, and the chosen distance metric). 

**Recommended Action:** Validate on independently constructed or debiased datasets (addressed in Section 5).

---

## Section 2: Impact Analysis (Record-Level Changes vs. Baseline)

**Impact** is defined as the net change in resolved records when comparing a candidate model to the chosen baseline. In other words, how many identity links does the new model *add* or *remove* relative to the baseline?

To quantify this rigorously, we partition outcomes into four mutually exclusive categories that together describe the complete Venn diagram of model outputs:

| Category | Set Operation | Description | Business Meaning |
|----------|---------------|-------------|------------------|
| **Model == Baseline** | Intersection | Records where both models produce identical output (including agreement on NULL) | No change; stable decisions |
| **Model != Baseline (non-null)** | Symmetric difference (non-null subset) | Records where the two models disagree but the variant still produces a non-NULL prediction | Changed but still resolved |
| **Model NULL & Baseline NOT NULL** | Baseline \ Model | Records resolved by baseline but dropped to NULL by the variant | Coverage loss / potential false negatives introduced |
| **Model NOT NULL & Baseline NULL** | Model \ Baseline | Records resolved by the variant that baseline missed | Coverage gain / potential new true positives |

### Results (2026-05-18 Data)

- The **baseline model** produced the most balanced impact profile: high agreement rate with itself (by definition) and the smallest disruptive changes when used as reference.
- Variants that changed the functional form introduced noticeably higher volumes of additions and removals, particularly in the "coverage loss" and "coverage gain" quadrants.
- Net effect: The default formulation minimizes unnecessary churn in identity resolution decisions.

**Interpretation**  
These impact results again point to the baseline as the most performant (or least disruptive) option **on the current data**. Combined with Section 1, this strengthens the hypothesis that **dataset bias may be present** — the data may reward models that closely mirror the original gravity assumptions.

---

## Section 3: Temporal Stability — F1-Score as a Function of Time (Drift Proxy)

The baseline model was executed across a longitudinal dataset covering approximately **one full year** of identity resolution events.

F1-score was computed within successive time windows (e.g., monthly or quarterly slices) to serve as a **proxy for model drift**.

### Objective
Detect whether model performance degrades over time due to:
- Shifting customer behavior
- Changes in store mix or revenue patterns
- Evolution of the distance/dissimilarity metric distributions

### Results

**F1-Score Trend Over Time**  
*(Attach line chart: F1-score on y-axis, time on x-axis with clear trend line and confidence band)*

**Key Finding:**  
A **slight downward drift** in F1-score was observed across the one-year period.

**Implications**
- The model is **not perfectly stationary**.
- Performance erosion, while modest, is measurable and should be monitored in production.
- Periodic recalibration or retraining is likely warranted (e.g., quarterly or triggered by drift thresholds).

---

## Section 4: Impact as a Function of Time

Using the same ~1-year longitudinal dataset, we extended the impact analysis (Section 2) to examine how record additions and removals evolve over time for each model variant.

### Results
- The **default gravity model (G = M1 × M2 / r²)** maintained the most stable and favorable impact characteristics across temporal slices.
- Alternative formulations exhibited greater volatility — larger swings in the volume of records added or removed in different time periods.
- This temporal consistency further supports the baseline as the currently strongest performer **on this dataset**.

### Consolidated Conclusion (Sections 1–4)
Taken together, the F1-score comparisons, impact (Venn) analysis, and temporal evaluations converge on the same observation:

> **Either** the default gravity model `G = M1 × M2 / r²` is genuinely the most performant formulation for this identity resolution task,  
> **or** there is **bias in the original evaluation dataset** that systematically favors the baseline.

To resolve this ambiguity, a controlled follow-up experiment using a deliberately debiased dataset was conducted (Section 5).

---

## Section 5: Debiased Dataset Experiment and Hybrid Model Performance

### Motivation
To test the bias hypothesis, a **new evaluation dataset** was constructed with **additional filters explicitly designed to remove or mitigate gravity-dependent signals**. Examples of such filters include:
- Down-weighting or excluding features directly derived from store revenue concentration
- Neutralizing customer spend density signals
- Introducing orthogonal behavioral or contextual features less correlated with the classic `M1 × M2 / r²` form

All five models (plus hybrid constructions) were re-evaluated on this debiased dataset at **two independent test dates**:
- 2026-06-03
- 2026-03-02

### Results

**Hybrid Model Performance vs. Baseline**

| Test Date     | Best Performing Model | F1-Score Lift vs. Baseline | Notes |
|---------------|-----------------------|----------------------------|-------|
| 2026-06-03    | **Hybrid Model**      | **+8.7%**                  | Strongest lift observed |
| 2026-03-02    | **Hybrid Model**      | **+4.2%**                  | Consistent positive lift |

*(Attach comparative bar chart or table visualization for both dates, including all five models + hybrid)*

**Key Finding:**  
The **hybrid model** (gravity scoring combined with complementary non-gravity signals or alternative scoring logic) **outperformed the baseline on both test dates**, with lifts of **8.7%** and **4.2%** respectively.

### Interpretation
This result provides **strong evidence that bias was present in the original dataset**. When gravity-correlated features were deliberately attenuated, the pure baseline model lost its artificial advantage. The hybrid formulation demonstrated superior robustness and generalization.

**Business Implication**  
The hybrid approach appears to be the most performant and least biased solution identified to date. It should be prioritized for further validation and potential production deployment.

---

## Overall Conclusions & Recommendations

### Summary of Findings
1. On the original dataset, the classic gravity model `G = M1 × M2 / r²` was the strongest performer across F1-score and impact metrics (Sections 1–4).
2. Temporal analysis revealed **mild model drift** over a one-year window.
3. When evaluated on a **debiased dataset** (gravity signals deliberately reduced), a **hybrid model** delivered clear improvements: **+8.7%** (2026-06-03) and **+4.2%** (2026-03-02) F1-score over baseline.
4. **Primary Conclusion:** Dataset bias likely inflated the apparent performance of the pure gravity formulation. The hybrid model is currently the most promising direction.

### Recommended Next Steps
- **Adopt Hybrid Model** as the leading candidate for identity resolution scoring. Proceed to A/B testing and shadow deployment.
- **Strengthen Drift Monitoring**: Implement automated tracking of F1-score and impact metrics over rolling time windows with alerting thresholds.
- **Dataset Bias Audit**: Apply gravity-decoupling filters more broadly during training data construction and ongoing evaluation.
- **Full Model Documentation**: Capture the exact mathematical definitions of all five variants and the final hybrid formulation for reproducibility and governance.
- **Production Validation**: Run controlled online experiments comparing baseline vs. hybrid in live traffic. Measure both offline metrics (F1) and online business KPIs (match rate, false positive rate, downstream system impact).
- **Expand Testing**: Validate hybrid performance across additional regions, customer segments, and longer time horizons.
- **Feature Engineering**: Continue exploring orthogonal signals that complement (rather than duplicate) gravity-based features.
