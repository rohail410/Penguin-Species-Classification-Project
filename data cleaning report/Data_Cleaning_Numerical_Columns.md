# Data Cleaning Report — Numerical Columns

**Notebook:** project.ipynb
**Dataset:** data/Penguin Species Prediction Dataset.csv (loaded as `df`)
**Date:** 2026-09-26
**Numerical columns identified:** `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g` — all already `float64`; no numeric-looking string columns or ID/date columns were found, so no dtype correction was needed to qualify any column for this list. The list was confirmed with the user before cleaning began.

## 1. Missing Values

- Each of the 4 numerical columns has exactly 10 missing values (1.0% each), spread across 40 distinct rows (4.0% of the dataset). Every affected row is missing exactly one of the four numeric measurements — no row is missing more than one — and the missingness shows no obvious pattern by species, island, or sex.
- **Decision:** leave missing values as `np.nan`. No imputation and no row drops, matching how the `sex` column's missing values were handled in the earlier categorical cleaning pass. This keeps the missingness explicit rather than baking an imputation choice into the cleaned data.
- Rows affected: 40 (1 missing value each, one of the 4 numeric columns).

## 2. Data Types

- All four columns are `float64`, matching their nature as continuous physical measurements. No numeric column was stored as text, and no integer-coded column was mistakenly numeric or categorical.
- **No action needed.**

## 3. Impossible / Invalid Values

- No column contains negative or zero values. Minimums are all biologically plausible (e.g. `body_mass_g` min 2830g, `flipper_length_mm` min 175mm).
- **No action needed.**

## 4. Outliers

- Dataset-wide IQR flagged 6 `body_mass_g` values as outliers, all belonging to `Gentoo` — the largest of the three species — so this is a species-scale effect, not a data error (Gentoo penguins are known to run substantially heavier than Adelie or Chinstrap).
- Re-running IQR within each species still surfaces a handful of mild outliers per column (a few unusually long/short culmen measurements, a couple of light/heavy Gentoo body masses), but every flagged value stayed within the biologically plausible range confirmed in steps 3 and 10 — none were impossible or clearly erroneous.
- **Decision (user-confirmed):** keep all values; flag only, no capping or row removal. These reflect natural biological variation between species and individuals, not data-entry errors.
- Rows affected: 0 changed (outliers documented, not modified).

## 5. Duplicate / Repeated Values

- No full-row duplicates, and no rows share identical values across all four numerical columns.
- **No action needed.**

## 6. Value Ranges and Distributions

- Ranges are tight and consistent with a single measurement protocol: `culmen_length_mm` 32.4–56.0, `culmen_depth_mm` 13.0–21.4, `flipper_length_mm` 175–235, `body_mass_g` 2830–6317.
- Per-species breakdowns show the expected separation: Gentoo is heavier and longer-flippered but has a shallower culmen than Adelie/Chinstrap. Distributions are unimodal within each species, with no gaps or multi-modal clusters suggesting mixed populations or a data-merging issue.
- Pure reporting step — no changes applied.

## 7. Units / Scale Consistency

- Checked for signs of mixed units (e.g. some rows recorded in cm or kg instead of mm/g) by looking for anomalously small values relative to each column's median. None were found. Column names already state a single unit each, and every value is consistent with that unit throughout.
- **No unit-inconsistency issue found; step not applicable to this dataset.**

## 8. Suspicious / Extreme Values

- Checked for over-represented exact values that might indicate placeholder/default data. The most frequent single value in any column was `189.0mm` in `flipper_length_mm` at 4.9% of rows — a plausible common measurement, not a red-flag round number.
- Checked decimal-place consistency: `culmen_length_mm`/`culmen_depth_mm` are recorded to 1 decimal place (with some whole numbers, as expected from real-world measurement rounding); `flipper_length_mm`/`body_mass_g` are consistently whole numbers. No mixed-precision pattern suggesting inconsistent recording.
- **Nothing suspicious found beyond the outliers already flagged and kept in step 4.**

## 9. Transformations

- Skewness is mild across all columns (|skew| < 1): `body_mass_g` (0.90) and `flipper_length_mm` (0.57) are the most right-skewed, driven by the heavier-bodied Gentoo species; `culmen_length_mm` and `culmen_depth_mm` are close to symmetric.
- **Recommendation (not applied, per user request):** no modeling code exists yet in the notebook, so no transformation was applied.
  - Tree-based models (Random Forest, Gradient Boosting, etc.) need no scaling or log-transform — they're invariant to monotonic feature transforms.
  - Distance-based or linear models (KNN, SVM, Logistic Regression, etc.) will need `StandardScaler`/`MinMaxScaler` at the modeling stage, since the columns are on very different scales (millimeters vs. grams). A log transform on `body_mass_g` could modestly reduce its right skew but is optional given how mild the skew is.
- This decision is deferred to the modeling stage.

## 10. Domain Knowledge Verification

- Per-species ranges match the well-documented Palmer Penguins dataset this appears to derive from: Gentoo (Biscoe island) is the heaviest (mean ~5058g) with the longest flippers and shallowest culmen depth; Adelie and Chinstrap are lighter (means ~3705g and ~3734g) with deeper culmens; Chinstrap has the longest average culmen length. All values fall within ranges reported in the original Palmer Station research for these three species.
- Nothing required further domain input beyond confirming this match.

## Summary of Changes

| Column | Issue | Action Taken | Rows Affected |
|---|---|---|---|
| `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g` | Missing values (1% each) | Left as `np.nan` — no imputation, no drop | 40 |
| `body_mass_g` (Gentoo) + mild per-species outliers across all 4 columns | Outliers (IQR) | Flagged only, kept as-is | 0 |
| All 4 columns | Data types, impossible values, duplicates, units | Checked — no issues found | 0 |
| All 4 columns | Transformation (scaling/log) | Recommended for modeling stage only, not applied | 0 |

## Open Questions / Needs Domain Input

None. All 10 checklist steps were reviewed; domain-knowledge verification (step 10) confirmed the data matches expected Palmer Penguins biology with no unresolved discrepancies.
