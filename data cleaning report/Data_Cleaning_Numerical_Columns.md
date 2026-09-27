# Data Cleaning Report — Numerical Columns

**Notebook:** project.ipynb
**Dataset:** `data/Penguin Species Prediction Dataset.csv` (loaded into `df`)
**Date:** 2026-09-27
**Numerical columns identified:** `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g` — all already `float64`, no dtype correction needed.

## 1. Missing Values
- 10 missing values (1.0%) in each of the 4 numerical columns. Missingness is scattered mostly across different rows, consistent with the overall pattern already documented in `Feature_Description.md` (951 rows fully complete, 48 rows with exactly one missing value, 1 row with two).
- **Decision:** left as `np.nan`. Not imputed (median, mean, or group-by-species), not dropped. Rationale: 1% per column isn't worth discarding rows over; imputing a bill/flipper/mass measurement risks inventing a value that was never observed; and the planned downstream models (XGBoost/LightGBM) handle `NaN` natively. This mirrors the decision already made for the `sex` column during categorical cleaning.
- Rows/cells affected: 10 per column (40 cells total across the 4 columns), 0 rows dropped.

## 2. Data Types
- All 4 columns are `float64`. No numeric-looking values were stored as strings/objects, and none of these should be integer or datetime instead.
- No action needed.

## 3. Impossible / Invalid Values
- Checked for negative and zero values in all 4 columns (physically impossible for bill length/depth, flipper length, or body mass).
- Result: 0 negative values, 0 zero values in every column.
- No action needed.

## 4. Outlier Detection
- Used the IQR method (1.5×IQR beyond Q1/Q3), computed both across the whole dataset and per species (since species is known for every row and body size genuinely differs by species — a large Gentoo isn't an anomaly the way a large Adelie would be).
- Whole-dataset IQR: 0 outliers in `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`; 6 outliers in `body_mass_g` (all Gentoo, up to 6317g).
- Per-species IQR (totals across the 3 species): `culmen_length_mm` 6, `culmen_depth_mm` 4, `flipper_length_mm` 2, `body_mass_g` 12.
- **Decision:** keep all values as-is — no capping, no removal. The whole-dataset `body_mass_g` outliers are a species effect (Gentoo is the largest of the three species and 6317g is consistent with the ~6300g maximum documented for Gentoo in the well-known Palmer Archipelago source data), not a data error. The smaller per-species outlier counts are normal distribution tails, not implausible values.
- Rows/cells affected: 0 (no changes made).

## 5. Duplicate Values
- Full-row duplicates were already checked earlier in the notebook (0 found).
- Checked again restricted to just the 4 numerical columns (in case two different penguins share identical measurements): 0 duplicates found.
- No action needed.

## 6. Value Ranges & Distributions
- Per-species min/max/mean:

| species | culmen_length_mm | culmen_depth_mm | flipper_length_mm | body_mass_g |
|---|---|---|---|---|
| Adelie | 32.4–44.8 (mean 38.87) | 15.6–21.4 (mean 18.28) | 175.0–205.0 (mean 189.85) | 2830–4550 (mean 3705.11) |
| Chinstrap | 40.9–56.0 (mean 48.80) | 15.8–20.9 (mean 18.34) | 175.0–214.0 (mean 195.64) | 2879–4591 (mean 3733.94) |
| Gentoo | 38.2–54.0 (mean 47.39) | 13.0–17.2 (mean 14.95) | 201.0–235.0 (mean 217.35) | 3623–6317 (mean 5058.39) |

- Distributions (see boxplot/histogram panels in the Exploratory Data Analysis section) are roughly unimodal per species with no extreme skew.

## 7. Inconsistent Units / Scales
- Not applicable. There's a single column per measurement (no parallel imperial-unit columns to reconcile), and the per-species ranges above show each column occupying one consistent, plausible scale — no stray low-magnitude values suggesting a unit mix (e.g. kg values mixed into `body_mass_g`).
- Skipped; nothing to standardize.

## 8. Suspicious / Extreme Values
- Checked measurement precision as an extra signal: `flipper_length_mm` and `body_mass_g` are whole numbers (0 non-integer values), while `culmen_length_mm` and `culmen_depth_mm` carry one decimal place (878 and 874 non-integer values respectively out of 990) — consistent with typical field-measurement precision (nearest mm/g for flipper/mass, nearest 0.1mm from calipers for bill measurements). No column mixes precisions in a way suggesting merged sources or unit drift.
- No action needed.

## 9. Transformations
- **Decision:** no transformation applied (no log, no scaling). Distributions are roughly unimodal per species with no extreme skew, and the categorical columns were already converted to `category` dtype specifically to feed tree-based models (XGBoost/LightGBM), which are invariant to monotonic transforms and feature scale. Scaling or log-transforming would add a step with no modeling benefit and would reduce interpretability of the raw measurements.

## 10. Domain Knowledge Verification
- All 4 columns' per-species ranges (Step 6) line up with the well-known Palmer Archipelago penguins reference ranges: Adelie/Chinstrap culmen length in the high-30s/low-40s to high-40s/low-50s mm, Gentoo distinctly longer-billed-but-shallower and heavier, flipper length increasing Adelie < Chinstrap < Gentoo, and body mass Gentoo well above the other two — matching expected biology (Gentoo is the largest of the three species, Adelie the smallest-billed).
- Nothing here needed to be flagged back to the user as implausible.

## Summary of Changes

| Column | Issue | Action Taken | Rows Affected |
|---|---|---|---|
| culmen_length_mm | 10 missing values (1.0%) | Left as `np.nan` | 10 |
| culmen_depth_mm | 10 missing values (1.0%) | Left as `np.nan` | 10 |
| flipper_length_mm | 10 missing values (1.0%) | Left as `np.nan` | 10 |
| body_mass_g | 10 missing values (1.0%); 6 whole-dataset IQR outliers (all Gentoo) | Left as `np.nan`; outliers kept as-is (species effect) | 10 |
| All 4 columns | Mild per-species IQR outliers (2-12 rows/column) | Kept as-is (normal distribution tails, not errors) | 0 rows changed |

No rows were dropped and no values were modified during numerical cleaning — every finding above resolved to "leave as observed."

## Open Questions / Needs Domain Input
None. All ranges and extremes were verifiable against known Palmer Archipelago penguin biology and matched expectations.
