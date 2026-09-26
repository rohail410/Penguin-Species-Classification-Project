# Categorical Data Cleaning Report

*Dataset: `<variable/file name>` · Generated: `<date>` · Last updated: `<date>`*

## 1. Overview

One short paragraph: what dataset this is, how many rows, which columns were treated as categorical, and the overall scale of issues found (e.g., "6 categorical columns reviewed; 3 required standardization, 1 had a meaningful missing-value problem").

## 2. Summary table

A quick-scan table, one row per categorical column, so a reader can see the shape of the whole cleaning pass at a glance before deciding which column sections to read in full.

| Column | # Unique (before → after) | Missing % | Key issues found | Action taken |
|---|---|---|---|---|
| `example_col` | 42 → 18 | 3.2% | Spelling variants, 5 rare categories | Merged variants, grouped rare into "Other" |

## 3. Column-by-column details

Repeat this section for every categorical column touched (including columns reviewed but left unchanged — note that explicitly rather than omitting them, so the report is a complete record).

### `<column_name>`

**What this column represents:** one line, from the user's domain knowledge if available.

**1. Missing/unknown values**
- Count and % missing (including disguised nulls like `"N/A"`, `"-"`, `"unknown"`)
- Decision made and why (e.g., "Kept as explicit 'Missing' category — user noted absence is meaningful here")

**2. Formatting standardization**
- What was normalized (case, whitespace, punctuation)
- Example before → after values

**3. Category name standardization**
- Variants found and merged, with counts, e.g.:
  - `"NY"` (312) + `"New York"` (890) → `"New York"` (1202)
- Reasoning for each merge (or for declining to merge something that looked similar but wasn't)

**4. Category validation**
- Any invalid/unexpected values found and how they were resolved

**5. Distribution**
- Value counts / percentages after cleaning (a short table or top-N list is fine; full distributions can live in the notebook)

**6. Cardinality**
- Unique count before and after cleaning, and whether that's expected for this column

**7. Rare category handling**
- Threshold used and why (count-based, %-based, top-N)
- What happened to values below the threshold (grouped into "Other", left alone, dropped — and why)

**8. Domain consistency check**
- What was checked against domain expectations, and the outcome (confirmed fine / flagged and resolved / flagged and left for user follow-up)

---

*(repeat "3. Column-by-column details" per column)*

## 4. Open questions / follow-ups

Anything flagged during cleaning that the user hasn't resolved yet, or judgment calls that may be worth revisiting later. Remove this section if there are none.

## 5. Revision history

Append an entry here every time the notebook/report is updated after the initial pass — don't rewrite earlier entries.

| Date | Change | Reason |
|---|---|---|
| `<date>` | Initial cleaning pass | — |
