# Categorical Data Cleaning Report

*Dataset: `df` (`data/Penguin Species Prediction Dataset.csv`) · Generated: 2026-09-26 · Last updated: 2026-09-26*

## 1. Overview

The dataset has 1,000 rows and 3 categorical (object-dtype) columns: `species`, `island`, and `sex`. This appears to derive from the well-known Palmer Penguins dataset (Palmer Station, Antarctica LTER). All three columns reviewed were already clean — no formatting noise, spelling/abbreviation variants, invalid categories, or rare categories were found. The only notable issue is 10 missing values (1.0%) in `sex`, which were confirmed as real `NaN`s and left as-is per the user's decision.

## 2. Summary table

| Column | # Unique (before → after) | Missing % | Key issues found | Action taken |
|---|---|---|---|---|
| `species` | 3 → 3 | 0.0% | None | None — already clean |
| `island` | 3 → 3 | 0.0% | None | None — already clean |
| `sex` | 2 → 2 | 1.0% | 10 real `NaN` values | Left as `np.nan` (no imputation, no drop, no "Missing" label) |

## 3. Column-by-column details

### `species`

**What this column represents:** the penguin's species — the target/label for this classification project.

**1. Missing/unknown values**
- 0 missing, 0 disguised placeholders (`"NA"`, `"-"`, `"unknown"`, etc.)
- No decision needed.

**2. Formatting standardization**
- Raw vs. whitespace-trimmed/lowercased unique counts matched (3 = 3) — no whitespace, casing, or punctuation issues.

**3. Category name standardization**
- Fuzzy-matching (difflib, threshold 0.6) found no near-duplicate pairs among `Adelie`, `Gentoo`, `Chinstrap` — all genuinely distinct.

**4. Category validation**
- All observed values are within the expected set `{Adelie, Gentoo, Chinstrap}`.

**5. Distribution**
- Adelie 461 (46.1%), Gentoo 288 (28.8%), Chinstrap 251 (25.1%)

**6. Cardinality**
- 3 unique values before and after — expected for a 3-species classification target.

**7. Rare category handling**
- Threshold: 5% of rows. Smallest category (Chinstrap, 25.1%) is far above it — no rare-category handling applied.

**8. Domain consistency check**
- All three values match the known Palmer Penguins species. Confirmed fine.

---

### `island`

**What this column represents:** the Palmer Station study island where the penguin was observed.

**1. Missing/unknown values**
- 0 missing, 0 disguised placeholders.

**2. Formatting standardization**
- Raw vs. normalized unique counts matched (3 = 3) — no issues.

**3. Category name standardization**
- No near-duplicate pairs found among `Torgersen`, `Biscoe`, `Dream`.

**4. Category validation**
- All observed values are within the expected set `{Torgersen, Biscoe, Dream}`.

**5. Distribution**
- Dream 527 (52.7%), Biscoe 302 (30.2%), Torgersen 171 (17.1%)

**6. Cardinality**
- 3 unique values before and after — expected (there are exactly 3 study islands in this dataset's domain).

**7. Rare category handling**
- Threshold: 5% of rows. Smallest category (Torgersen, 17.1%) is well above it — no rare-category handling applied.

**8. Domain consistency check**
- All three values match the known Palmer Station study islands. Confirmed fine.

---

### `sex`

**What this column represents:** the penguin's biological sex.

**1. Missing/unknown values**
- 10 missing (1.0%), stored as real `NaN`, 0 disguised placeholders.
- **Decision (user-confirmed):** leave as `np.nan` — no imputation, no row drop, no explicit `"Missing"` category.

**2. Formatting standardization**
- Raw vs. normalized unique counts matched (2 = 2) — no issues.

**3. Category name standardization**
- No near-duplicate pairs found between `Male` and `Female`.

**4. Category validation**
- All observed non-null values are within the expected set `{Male, Female}`.

**5. Distribution**
- Male 528 (52.8%), Female 462 (46.2%), missing 10 (1.0%)

**6. Cardinality**
- 2 unique values before and after — expected for a binary sex field.

**7. Rare category handling**
- Threshold: 5% of rows. Smallest non-missing category (Female, 46.2%) is far above it — no rare-category handling applied.

**8. Domain consistency check**
- Both values match the two expected biological sex categories. Confirmed fine.

---

## 4. Open questions / follow-ups

None. All 8 steps were reviewed for each column; no unresolved judgment calls remain.

## 5. Revision history

| Date | Change | Reason |
|---|---|---|
| 2026-09-26 | Initial cleaning pass | — |
