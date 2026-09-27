# Categorical Data Cleaning Report

*Dataset: `df` (`data/Penguin Species Prediction Dataset.csv`) · Generated: 2026-09-27 · Last updated: 2026-09-27*

## 1. Overview

The dataset has 1,000 rows and 3 categorical columns: `species`, `island`, and `sex`. This matches the structure of the well-known Palmer Penguins dataset. All three columns reviewed came back clean — no whitespace/case inconsistencies, no spelling/abbreviation variants, no invalid categories, and no rare-category problem. The only issue found was 10 missing values (1.0%) in `sex`, which was left as `NaN` at the user's request pending a modeling-stage decision. All three columns were converted to pandas `category` dtype.

## 2. Summary table

| Column | # Unique (before → after) | Missing % | Key issues found | Action taken |
|---|---|---|---|---|
| `species` | 3 → 3 | 0.0% | None | None — reviewed and confirmed clean |
| `island` | 3 → 3 | 0.0% | None | None — reviewed and confirmed clean |
| `sex` | 2 → 2 | 1.0% | 10 missing values | Left as `NaN`, deferred to modeling stage |

## 3. Column-by-column details

### `species`

**What this column represents:** the penguin's species — the target/label column for this classification project.

**1. Missing/unknown values**
- 0 nulls, 0 placeholder-junk values (checked for `""`, `"NA"`, `"N/A"`, `"none"`, `"null"`, `"-"`, `"unknown"`, `"?"`, `"9999"`).
- No decision needed.

**2. Formatting standardization**
- No whitespace, double-space, or case issues found. Values already consistent: `Adelie`, `Gentoo`, `Chinstrap`.
- No changes applied.

**3. Category name standardization**
- Fuzzy-similarity check across the 3 unique values found no near-duplicate pairs.
- No merges applied.

**4. Category validation**
- Actual values (`Adelie`, `Chinstrap`, `Gentoo`) checked against the known valid set for this domain — no invalid values found.

**5. Distribution**
| Value | Count | % |
|---|---|---|
| Adelie | 461 | 46.1% |
| Gentoo | 288 | 28.8% |
| Chinstrap | 251 | 25.1% |

**6. Cardinality**
- 3 unique values before and after — expected for a species label.

**7. Rare category handling**
- No threshold needed — smallest category (Chinstrap, 25.1%) is far from rare.

**8. Domain consistency check**
- Matches the 3 known Palmer Penguins species exactly. Confirmed fine.

---

### `island`

**What this column represents:** the island in the Palmer Archipelago where the penguin was observed.

**1. Missing/unknown values**
- 0 nulls, 0 placeholder-junk values.
- No decision needed.

**2. Formatting standardization**
- No whitespace, double-space, or case issues found. Values already consistent: `Torgersen`, `Biscoe`, `Dream`.
- No changes applied.

**3. Category name standardization**
- Fuzzy-similarity check across the 3 unique values found no near-duplicate pairs.
- No merges applied.

**4. Category validation**
- Actual values (`Biscoe`, `Dream`, `Torgersen`) checked against the known valid set for this domain — no invalid values found.

**5. Distribution**
| Value | Count | % |
|---|---|---|
| Dream | 527 | 52.7% |
| Biscoe | 302 | 30.2% |
| Torgersen | 171 | 17.1% |

**6. Cardinality**
- 3 unique values before and after — expected for an island field.

**7. Rare category handling**
- No threshold needed — smallest category (Torgersen, 17.1%) is far from rare.

**8. Domain consistency check**
- Matches the 3 known Palmer Archipelago islands exactly. Confirmed fine.

---

### `sex`

**What this column represents:** the penguin's sex.

**1. Missing/unknown values**
- 10 nulls (1.0% of rows), 0 placeholder-junk values.
- **Decision (confirmed with user):** leave the 10 `NaN` values untouched for this cleaning pass — no imputation, no explicit `"Missing"` category. The handling decision is deferred to the modeling/imputation step.

**2. Formatting standardization**
- No whitespace, double-space, or case issues found. Values already consistent: `Female`, `Male`.
- No changes applied.

**3. Category name standardization**
- Fuzzy-similarity check flagged `'Female'` vs `'Male'` (similarity 0.80) — reviewed and determined to be a false positive of character-level string similarity, not a real spelling/abbreviation variant. Male and Female are genuinely distinct categories.
- No merges applied.

**4. Category validation**
- Actual values (`Female`, `Male`) checked against the known valid set for this domain — no invalid values found.

**5. Distribution** (including missing)
| Value | Count | % |
|---|---|---|
| Male | 528 | 52.8% |
| Female | 462 | 46.2% |
| *(missing)* | 10 | 1.0% |

**6. Cardinality**
- 2 unique values before and after — expected for a binary sex field.

**7. Rare category handling**
- No threshold needed — both categories are well-represented.

**8. Domain consistency check**
- Binary Male/Female matches domain expectations for this dataset. Confirmed fine.

## 4. Dtype conversion

| Column | Converted to `category`? | Notes |
|---|---|---|
| `species` | Yes | User opted to convert all three columns; supports native categorical handling in tree-based models (XGBoost/LightGBM with `enable_categorical=True`, CatBoost) and is more memory-efficient. |
| `island` | Yes | Same as above. |
| `sex` | Yes | Same as above. Note: the `category` dtype still represents the 10 missing values as `NaN`. |

## 5. Open questions / follow-ups

- **`sex` missing values (10 rows, 1.0%):** left as `NaN` by user decision. Needs a final call (impute, explicit "Missing" category, or drop) before/during modeling, since some pipelines and encoders handle `NaN` in a `category` column differently than others.

## 6. Revision history

| Date | Change | Reason |
|---|---|---|
| 2026-09-27 | Initial cleaning pass | — |
