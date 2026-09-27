# Data Cleaning Report — Numerical Columns

**Notebook:** `project.ipynb`
**Dataset:** `df` (`data/Penguin Species Prediction Dataset.csv`)
**Date:** 2026-09-27
**Numerical columns identified:** `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g` — all already `float64`, no dtype correction needed to qualify them.

## 1. Missing Values

Each of the four columns has exactly 10 missing values (1.0% each, 40 rows total). The missingness is scattered: each affected row is missing exactly one of the four measurements — none of the 40 rows has more than one missing value, and there's no overlap in pattern with the 10 `NaN`s in `sex` (from the categorical cleaning pass). This looks like independent, random single-field dropout (e.g. an unrecorded measurement) rather than a systemic issue tied to a species, island, or measurement session.

**Decision (confirmed with user):** leave all 40 missing values as `NaN` — no imputation applied in this pass. This mirrors how `sex`'s missing values were handled in categorical cleaning; the decision is deferred to the modeling/imputation step.

**Rows affected:** 40 (4.0% of the dataset), each with exactly 1 of 4 fields missing.

## 2. Data Types

All four columns are already `float64` — no numbers-as-strings, no dates or codes stored as numbers. No action needed.

## 3. Impossible / Invalid Values

Checked for physically impossible values (≤ 0 for any measurement) and cross-checked min/max against a broad plausibility band for Palmer Penguins measurements (`culmen_length_mm` 30–62, `culmen_depth_mm` 12–22, `flipper_length_mm` 170–235, `body_mass_g` 2500–6400).

- 0 values ≤ 0 in any column.
- 0 values outside the plausibility band.

No invalid values found; no action needed.

## 4. Outliers

Used the IQR method (1.5×IQR fences), computed both across the whole dataset and within each species (mixing species together makes normal cross-species differences look like outliers).

- **Whole-dataset IQR:** only `body_mass_g` flags outliers — 6 high values (6114–6317 g), all Gentoo (the heaviest species). Not true anomalies, just Gentoo's natural weight range appearing extreme against the pooled distribution.
- **Per-species IQR:** 24 distinct rows flagged as an outlier on at least one column within their own species — mostly mild boundary cases (e.g. Adelie `culmen_length_mm` of 32.4–33.0mm, Gentoo `body_mass_g` in the high-5000s/low-6000s or low-3600s). None of these coincide with the Step 3 invalid-value/range findings.

**Decision (confirmed with user):** keep all 24 flagged rows as-is — no capping or removal. They read as genuine biological variation rather than data-entry errors, and removing/capping them risks discarding real signal for species classification.

**Rows affected:** 24 (2.4% of the dataset) — kept unchanged.

## 5. Duplicate / Repeated Values

Full-row duplicates were already checked in the initial data exploration section (0 found). Checked separately here:
- Rows with identical values across all 4 numeric columns (excluding rows with any missing value): **0**.
- Most-repeated single value per column: `flipper_length_mm = 189.0` (49 rows, 4.9%) — expected for a value rounded to the nearest millimeter across 1000 samples, not a placeholder constant.

No duplicate/repeated-value issues found; no action needed.

## 6. Value Ranges and Distributions

- **Skewness:** `culmen_length_mm` 0.08, `culmen_depth_mm` -0.49, `flipper_length_mm` 0.57, `body_mass_g` 0.90 (mildly right-skewed, driven by Gentoo's heavier weight pulling the tail).
- **Per-species means/stds** line up with the well-known Palmer Penguins structure: Gentoo is heaviest with the shallowest culmen depth and longest flippers; Adelie has the shortest culmen length; Chinstrap has the deepest/longest culmen.

No distributional red flags. Pure reporting — no changes applied.

## 7. Inconsistent Units / Scales

Checked for a low-value cluster that would suggest part of the data was recorded in a different unit (e.g. body mass in kg instead of g, or culmen length in cm instead of mm). No values fell anywhere near a plausible alternate-unit range for any column.

**Not applicable** — no unit-mixing detected across any of the four columns; nothing to convert.

## 8. Suspicious / Extreme Values

Beyond the mechanical IQR fences in Step 4, checked for individually-valid-but-jointly-odd combinations (e.g. a Gentoo-typical flipper length paired with an Adelie-typical body mass) using a stricter >3-standard-deviation-from-species-mean bar.

Only 4 rows exceeded this bar (rows 763, 767, 818, 860) — all a subset of the Step 4 per-species outlier list, and none showing an implausible *combination* of measurements. Nothing here points to a mislabeled species or swapped measurement; these are genuinely unusual individual birds, covered by the same "keep as-is" decision as Step 4.

## 9. Transformations

**Recommendation:** none of the four columns need a log transform — skewness is mild throughout (|skew| ≤ 0.9). If the downstream model is distance/gradient-based (logistic regression, KNN, SVM, neural nets), the columns are on very different scales (culmen depth ~13–22 vs. body mass ~2800–6300) and would benefit from `StandardScaler` or min-max scaling. If the plan is a tree-based model (XGBoost/LightGBM/Random Forest — consistent with the categorical columns already being converted to `category` dtype for such models), no scaling is needed at all.

**Decision (confirmed with user):** the downstream model choice hasn't been decided yet, so no transformation or scaling is applied in this pass. Revisit once the modeling approach is chosen.

## 10. Verify Against Domain Knowledge

Compared this dataset's per-species min/max against published Palmer Penguins reference ranges:

| Species | Reference culmen length | Reference culmen depth | Reference flipper length | Reference body mass |
|---|---|---|---|---|
| Adelie | ~32–46mm | ~15.5–21.5mm | ~172–210mm | ~2850–4775g |
| Chinstrap | ~40.9–58mm | ~16.4–20.8mm | ~178–212mm | ~2700–4800g |
| Gentoo | ~40.9–59.6mm | ~13.1–17.3mm | ~203–231mm | ~3950–6300g |

This dataset's observed ranges are broadly consistent, with two mild low-end deviations for Gentoo:
- `culmen_length_mm` minimum of 38.2mm (vs. ~40.9mm reference) — the same 2 rows flagged as outliers in Step 4.
- `body_mass_g` minimum of 3623g (vs. ~3950g reference) — overlaps with the low-end Gentoo outliers from Step 4 (3623, 3829, 3851g).

Both are plausible as natural low-end variation given this dataset's larger sample (1000 rows vs. ~344 in the original reference dataset), but are surfaced as open questions rather than assumed away.

## Summary of Changes

| Column | Issue | Action taken | Rows affected |
|---|---|---|---|
| `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g` | Missing values (1.0% each) | Left as `NaN`, deferred to modeling stage | 40 |
| `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g` | Per-species statistical outliers | Kept as-is — judged genuine biological variation | 24 |
| All four | Invalid values, duplicates, unit mismatches | None found | 0 |
| All four | Transformation/scaling | Not applied — deferred until model choice is made | 0 |

No values in the dataset were modified, imputed, capped, or removed during this pass.

## Open Questions / Needs Domain Input

1. **Missing values (40 rows, 1.0% per column):** left as `NaN`. Needs a final call (drop, impute, or model-native NaN handling) before/during modeling.
2. **Per-species outliers (24 rows) / suspicious extremes (4 of those 24):** kept as-is. If domain expertise suggests any of these are measurement errors rather than genuine variation, they should be revisited.
3. **Gentoo low-end deviations from published reference ranges** (`culmen_length_mm` min 38.2mm, `body_mass_g` min 3623g): plausible as natural variation in a larger sample, but not independently verified against a primary source for this specific dataset.
4. **Transformation/scaling strategy:** deferred until the downstream model type (tree-based vs. distance/gradient-based) is decided.

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-09-27 | Initial cleaning pass | — |
