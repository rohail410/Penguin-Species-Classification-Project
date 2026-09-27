# Categorical Data Cleaning Report

*Dataset: `df` (`data/Penguin Species Prediction Dataset.csv`) · Generated: 2026-09-27 · Last updated: 2026-09-27*

## 1. Overview

The dataset has 1,000 rows and 3 categorical columns: `species` (the prediction target), `island`, and `sex`. All three were already clean — no formatting inconsistencies, spelling variants, invalid categories, or rare categories were found. The only issue was 10 missing values (1%) in `sex`, which were left as `NaN` per the user's decision.

## 2. Summary table

| Column | # Unique (before → after) | Missing % | Key issues found | Action taken |
|---|---|---|---|---|
| `species` | 3 → 3 | 0% | None | None needed |
| `island` | 3 → 3 | 0% | None | None needed |
| `sex` | 2 → 2 | 1.0% | 10 missing values | Left as `NaN` (not imputed/dropped) |

## 3. Column-by-column details

### `species`

**What this column represents:** The prediction target — the penguin's species (Adelie, Gentoo, or Chinstrap).

**1. Missing/unknown values**
- 0 missing, 0 disguised-null placeholders (`"NA"`, `"unknown"`, `"?"`, etc.)

**2. Formatting standardization**
- Checked for whitespace/casing inconsistencies via `.str.strip()` + whitespace collapse — 0 values changed. Already consistently formatted (title case, no stray whitespace).

**3. Category name standardization**
- Fuzzy-matching pass (`difflib.get_close_matches`, cutoff 0.75) found no near-duplicate spellings among `Adelie`, `Gentoo`, `Chinstrap`.

**4. Category validation**
- Checked against the known valid set for this domain (`{Adelie, Gentoo, Chinstrap}`) — no invalid values found.

**5. Distribution**
| Category | Count | % |
|---|---|---|
| Adelie | 461 | 46.1% |
| Gentoo | 288 | 28.8% |
| Chinstrap | 251 | 25.1% |

**6. Cardinality**
- 3 unique values before and after — expected for a 3-species target column.

**7. Rare category handling**
- Threshold used: <5% of rows. No category fell below this threshold (smallest is Chinstrap at 25.1%), so nothing was grouped.

**8. Domain consistency check**
- Matches the three species (Adelie, Chinstrap, Gentoo) documented in the well-known Palmer Archipelago penguins dataset this data derives from. Confirmed fine.

---

### `island`

**What this column represents:** Which of three islands in the Palmer Archipelago the penguin was recorded on.

**1. Missing/unknown values**
- 0 missing, 0 disguised-null placeholders.

**2. Formatting standardization**
- Checked via `.str.strip()` + whitespace collapse — 0 values changed. Already consistent (title case, no stray whitespace).

**3. Category name standardization**
- Fuzzy-matching pass found no near-duplicate spellings among `Biscoe`, `Dream`, `Torgersen`.

**4. Category validation**
- Checked against the known valid set (`{Biscoe, Dream, Torgersen}`) — no invalid values found.

**5. Distribution**
| Category | Count | % |
|---|---|---|
| Dream | 527 | 52.7% |
| Biscoe | 302 | 30.2% |
| Torgersen | 171 | 17.1% |

**6. Cardinality**
- 3 unique values before and after — expected for the three islands in this dataset's collection area.

**7. Rare category handling**
- Threshold used: <5% of rows. No category fell below this threshold (smallest is Torgersen at 17.1%), so nothing was grouped.

**8. Domain consistency check**
- Matches the three islands (Biscoe, Dream, Torgersen) documented in the Palmer Archipelago penguins dataset. Confirmed fine.

---

### `sex`

**What this column represents:** The penguin's biological sex (Male/Female).

**1. Missing/unknown values**
- 10 missing (1.0% of rows), 0 disguised-null placeholders.
- **Decision (user):** left as real `NaN`, not imputed or dropped. Rationale: sex can't be reliably inferred from the bill/flipper/body-mass measurements alone, and 1% of rows isn't worth discarding.

**2. Formatting standardization**
- Checked via `.str.strip()` + whitespace collapse — 0 values changed. Already consistent (title case, no stray whitespace).

**3. Category name standardization**
- Fuzzy-matching pass found no near-duplicate spellings among `Male`, `Female`.

**4. Category validation**
- Checked against the known valid set (`{Male, Female}`) — no invalid values found (other than the expected `NaN`s).

**5. Distribution**
| Category | Count | % |
|---|---|---|
| Male | 528 | 52.8% |
| Female | 462 | 46.2% |
| NaN | 10 | 1.0% |

**6. Cardinality**
- 2 unique values (excluding `NaN`) before and after — expected for a binary sex field.

**7. Rare category handling**
- Threshold used: <5% of rows. Neither Male (52.8%) nor Female (46.2%) fell below this threshold, so nothing was grouped. (The `NaN`s are handled as missing values, not as a rare category.)

**8. Domain consistency check**
- Binary Male/Female values match expectations for a biological sex field. Confirmed fine.

---

## 4. Dtype conversion

| Column | Converted to `category`? | Notes |
|---|---|---|
| `species` | Yes | User confirmed conversion for all three columns, in preparation for tree-based models (e.g. XGBoost with `enable_categorical=True`) |
| `island` | Yes | Same as above |
| `sex` | Yes | Same as above |

## 5. Open questions / follow-ups

None.

## 6. Revision history

| Date | Change | Reason |
|---|---|---|
| 2026-09-27 | Initial cleaning pass | — |
