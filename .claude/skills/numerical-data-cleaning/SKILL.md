---
name: numerical-data-cleaning
description: Run a full numerical-column data cleaning pass on a Jupyter notebook (.ipynb) — missing values, dtype checks, invalid/impossible values, outliers, duplicates, distributions, unit inconsistencies, suspicious extremes, transformations, and domain-knowledge sanity checks — executing cells against the real data and writing a Data_Cleaning_Numerical_Columns.md report. Use this whenever the user asks to clean, audit, or validate the numerical columns in a notebook or dataframe, even if they only name one or two of the checklist items (e.g. "handle the missing values and outliers in this notebook") or just say "clean this dataset." Also use it for follow-up requests to revise, undo, or redo a cleaning decision made earlier — these update both the notebook and the existing report rather than starting over.
---

# Numerical Data Cleaning

Runs a structured, ten-point cleaning pass over the numerical columns of a dataset inside an existing Jupyter notebook, and keeps a running written record of every decision in a report the user can read, question, and ask you to change.

The two things this skill is protecting are **traceability** (the user should be able to see exactly what changed and why, in both the notebook and the report) and **judgment where judgment is due** (some steps are mechanical checks with one right answer; others are calls only the user can really make about their own data — don't guess on those).

## Before starting

1. Find the target notebook. If the user names one, use it; if there's exactly one `.ipynb` in the working context, confirm it's the right one; if there are several, ask which.
2. Read the notebook and run it (or run the relevant cells) so you're working from real, current output — not from assumptions about what the data looks like. A stale kernel state produces a report full of guesses. Use whatever run mechanism is available (an existing kernel, `jupyter nbconvert --to notebook --execute`, or `nbclient`) — pick whichever fits the notebook's existing setup rather than restarting the user's whole environment unless needed.
3. Identify the numerical columns. Don't rely on `dtype` alone — a column of `dtype: object` that's actually numbers stored as strings (`"1,204"`, `"$50"`, `"12 kg"`) is exactly the kind of thing step 2 of the checklist below exists to catch. Look at both declared dtypes and column content to build a candidate list.
4. **Confirm the candidate list with the user before doing any cleaning.** Show the columns you intend to treat as numerical (including any object-dtype columns you're including because they look numeric, and any numeric-looking columns you're excluding, e.g. an ID column, and why). Let them add, remove, or correct entries — they may know a column is actually categorical (a coded status field), or want one included/excluded that your heuristic got wrong. Don't proceed to step 1 of the checklist until this list is settled. Once confirmed, note the final list in the notebook.
5. Check whether `data cleaning report/Data_Cleaning_Numerical_Columns.md` already exists next to the notebook. If it does, this is a continuation or revision, not a fresh run — read it first (see "Revisions" below).

## Working in the notebook

- Clean in place on the working dataframe; there's no separate raw-data backup copy to maintain, so be deliberate — each change should be a distinct, re-runnable cell, not an in-place mutation buried inside a larger cell, so a step can be identified and revised later without re-running everything from scratch.
- Precede each checklist step with a markdown cell header (e.g. `## 3. Impossible/invalid values`) so the notebook itself reads as a narrative of the cleaning process, matching the report.
- Execute each cell as you add it. Decisions in later steps (e.g. outlier thresholds) often depend on what an earlier step's output actually showed, so don't write the whole notebook speculatively and run it at the end.
- Show your work: print or display the diagnostic output (missing counts, dtype summary, describe(), etc.) in the cell before the cell that acts on it, so the notebook's outputs are the evidence for the report's claims.

## The checklist

Go through these in order. For each one, the table below says whether it's a **check** (report findings, no data change, no need to ask) or an **action** (changes the data). For actions, the last column says whether to just do it or to ask first.

| # | Step | Type | Ask first? |
|---|------|------|------------|
| 1 | Handle missing values | action | **Yes** — drop vs. impute (and which method) changes the dataset's meaning; there's rarely one correct answer |
| 2 | Check and correct data types | check → action | No, if it's unambiguous (a numeric-looking string column, a date stored as int). Ask if the fix itself is a judgment call. |
| 3 | Identify impossible/invalid values (e.g. negative age) | check → action | **Yes** — deciding whether to null, drop, or clip an invalid value needs the user's context on the data |
| 4 | Detect outliers | check → action | **Yes** for what to do about them (keep, cap, remove). Detecting and reporting them is fine to do unprompted. |
| 5 | Check for duplicate/repeated values | check → action | Ask before dropping rows; flagging duplicates is fine unprompted |
| 6 | Check value ranges and distributions | check | No — this is pure reporting (min/max/quantiles/shape), nothing to apply |
| 7 | Handle inconsistent units/scales (e.g. kg vs lbs) | check → action | **Yes** — needs the user to confirm which unit is the target and confirm your read of which rows are in which unit |
| 8 | Check for suspicious/extreme values | check | No — reporting; overlaps with outliers but catches things like implausible-but-technically-valid values worth flagging for the user's domain knowledge |
| 9 | Decide whether transformations are needed (log, scaling, etc.) | recommendation | **Yes** — this depends entirely on what the user plans to do with the data downstream (modeling vs. reporting), so propose it, don't apply it silently |
| 10 | Verify values against domain knowledge | check | This one is really a question *for* the user — surface anything you can't judge yourself (e.g. "is a max order size of 50,000 units plausible for this business?") rather than guessing |

Batch your questions where you can. If steps 1, 3, and 4 all surfaced things needing a decision, ask them together in one round rather than stopping the user after every single step — but do ask before steps 6, 8, and 10's findings are the only place you can't batch anything, since they don't need any decision at all.

Skip a step only if it plainly doesn't apply (e.g. step 7 when nothing suggests mixed units) and say so in the report rather than silently omitting it — the user should see all ten were considered.

## The report

Location: `data cleaning report/Data_Cleaning_Numerical_Columns.md`, sitting alongside the notebook. Create the folder if it doesn't exist.

Write the report as you go, not as a final step reconstructed from memory — draft each step's section right after that step is done in the notebook, while the actual numbers are in front of you.

Structure:

```markdown
# Data Cleaning Report — Numerical Columns

**Notebook:** <filename>
**Dataset:** <source file / variable name>
**Date:** <date>
**Numerical columns identified:** <list, with a one-line note on any that needed dtype correction to qualify>

## 1. Missing Values
- What was found (counts/percentages per column)
- Decision made and why
- Rows/cells affected

## 2. Data Types
...

(one section per checklist step, in order; for a skipped step, say what was checked and why no action was needed)

## Summary of Changes
A short table: column | issue | action taken | rows affected

## Open Questions / Needs Domain Input
Anything from step 10 (or elsewhere) you couldn't resolve yourself.
```

Keep each section focused on what actually happened to *this* dataset — findings and the reasoning behind the decision — not a generic explanation of the technique. Someone re-reading it later should understand what was done to their data and why, without needing to already know what an IQR is.

## Revisions

When the user comes back later and asks to change something ("actually don't drop those outliers," "use mean instead of median for the missing ages"):

1. Read the existing report and find the relevant notebook cell(s) for that step.
2. Edit the notebook cell(s) in place and re-execute from that point forward — later steps may depend on the changed data, so re-run anything downstream of the change rather than only the one cell.
3. **Don't rewrite the report from scratch.** Update the specific section to reflect the new decision, and append a dated entry to a changelog section at the end of the report:

```markdown
## Changelog
### 2026-09-26 — Missing value strategy for `age`
Changed from median imputation to mean imputation at the user's request, because <reason if given>. Rows affected: <n>. Re-ran steps 3–10 downstream since the imputed values feed into outlier detection.
```

This keeps the report's main body an accurate description of the current state while preserving the history of why decisions changed — useful if the user (or a collaborator) wants to know the dataset's cleaning went through revisions and why.
