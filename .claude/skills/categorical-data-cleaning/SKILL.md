---
name: categorical-data-cleaning
description: Clean the categorical (text/object) columns of a dataset that is already loaded into a Jupyter notebook — handling missing values, inconsistent formatting, spelling/abbreviation variants, invalid categories, rare/high-cardinality categories, and domain-consistency checks. Adds new cells directly to the notebook and writes a companion Markdown report (Data_Cleaning_Categorical_Columns.md in a "data cleaning report" folder) documenting every change with before/after evidence. Use this whenever the user asks to clean, standardize, fix, or audit categorical/text columns in a notebook, asks about category distributions, rare categories, cardinality, or inconsistent category spellings, or asks to update/redo a categorical cleaning pass they ran earlier. Always prefer this skill over ad-hoc cleaning code for this kind of task, even if the user just says something like "can you clean up the string columns in this data" or "the category values are messy, can you sort them out."
---

# Categorical Data Cleaning

## What this skill does

Runs a structured, 8-step categorical-cleaning pass over the categorical (object/string) columns of a DataFrame that already exists in the user's notebook, adds the cleaning code as new cells in that same notebook, and produces a Markdown report that a non-technical stakeholder could read to understand exactly what changed and why.

The point of the structure below isn't to be followed like a rigid checklist for its own sake — categorical data breaks in a fairly predictable sequence of ways (missing values, then formatting noise, then near-duplicate spellings, then genuinely invalid values, then long-tail rarity), and cleaning them in that order matters: e.g., you can't sensibly judge cardinality or rare categories until formatting and spelling variants have already been merged, or you'll double-count "usa", "USA", and "U.S.A." as three separate rare categories. Use judgment about how deep to go on each step for a given column — a clean 3-value column doesn't need the same scrutiny as a messy 200-value free-text field.

## Before starting

1. **Find the DataFrame.** Look at the notebook's existing cells for a DataFrame already loaded (`pd.read_csv`, `pd.read_excel`, an existing `df = ...`, etc.). If there's exactly one obvious candidate, use it. If there are several DataFrames, or none visible, ask the user which variable to work on rather than guessing.
2. **Identify categorical columns.** Treat `object`/`string`/`category` dtype columns as candidates, plus any numeric-looking columns the user tells you are actually categorical codes (e.g., a `region_id` that's really a category). Show the user the list of columns you intend to treat as categorical before proceeding, so they can add/remove any.
3. **Check for a prior run.** Look for an existing `data cleaning report/Data_Cleaning_Categorical_Columns.md` in the project. If one exists, this is an **update**, not a fresh run — see "Updating a previous cleaning pass" below instead of starting over.
4. **Ask before acting on judgment calls.** Per column, several of the steps below involve a decision that isn't purely mechanical (is "NY" a typo for "New York" or a legitimate distinct category? should rare categories be merged into "Other", left alone, or dropped?). Surface these as concrete questions with the evidence attached (e.g., "Column `state` has both 'NY' (312 rows) and 'New York' (890 rows) — merge into 'New York'?") rather than deciding silently. Batch these questions per column or across a few similar columns so the user isn't answered one at a time for every tiny thing — but never apply a merge, drop, or rename without confirmation first. Purely mechanical steps (trimming whitespace, lowercasing for comparison, flagging nulls) don't need a check-in.

## The 8 cleaning steps

Work through these per categorical column. Add one notebook cell (or a small logical group of cells) per step, with a short markdown cell above each explaining what it's doing and why, so the notebook itself stays readable as a narrative rather than a wall of code.

1. **Missing/unknown values.** Find nulls, but also placeholder junk that means "missing" without being `NaN` — empty strings, `"NA"`, `"N/A"`, `"none"`, `"null"`, `"-"`, `"unknown"`, `"?"`, `"9999"`, etc. Report the count and percentage per column. Ask the user how they want missing values handled (leave as a real `"Missing"` category, impute with mode, drop rows) — the right answer depends on what the column means and how the data will be used, which the user knows and you don't.
2. **Standardize formatting.** Trim leading/trailing whitespace, collapse internal double-spaces, normalize case (usually title case or lowercase — pick whichever reads more naturally for that column, e.g. lowercase for codes, title case for names), and strip stray punctuation that isn't semantically meaningful. This step is almost always safe to apply directly since it doesn't change what a value *means*, just how it's written.
3. **Standardize category names (spelling/abbreviations/synonyms).** After formatting is normalized, look for values that are likely the same real-world category written differently — typos, abbreviations ("NY" / "New York"), synonyms ("Male" / "M"), or inconsistent casing that survived step 2. Use string similarity (e.g. fuzzy matching) as a starting point but don't blindly trust it — confirm groupings with the user before merging, especially where two values could plausibly be genuinely different things.
4. **Validate categories.** Check for values that shouldn't exist at all given the column's meaning — out-of-range codes, impossible values, or free text that leaked into what should be a controlled field. If the user has or knows a reference list of valid categories, validate against it; otherwise infer likely valid categories from frequency and flag outliers for the user to confirm.
5. **Check category distribution.** Compute value counts and percentages per column. This is diagnostic, not a change — it's what makes steps 6-7 possible to reason about, and it belongs in the report even for columns that end up needing no changes.
6. **Check cardinality.** Count unique categories per column. Flag columns with unexpectedly high cardinality for a "categorical" field (could indicate the column is actually closer to free text, or that step 3 missed some duplicates) and note it.
7. **Handle rare/high-cardinality categories.** Decide, with the user, what counts as "rare" for this dataset (a fixed count threshold, a percentage threshold, or "the long tail beyond the top N") and how to handle it — group into "Other", keep as-is if rarity is meaningful (e.g. rare disease categories shouldn't be lumped away), or something else. This is highly dataset-dependent, so don't apply a default threshold without asking.
8. **Verify consistency with domain knowledge.** Sanity-check the cleaned categories against what the user knows about the domain — e.g., does a `country` column's category list roughly match expected countries in the dataset's context? Does a `department` column match the departments the user says actually exist? Ask the user directly if anything looks off, since this step depends entirely on context you don't have.

## Writing to the notebook

- Use the notebook editing tool to append cells to the **existing** notebook the DataFrame came from — don't create a separate notebook.
- Structure: a markdown header cell ("## Categorical Data Cleaning") to open the section, then per-column (or per-step, whichever reads more naturally for the dataset) markdown + code cell pairs.
- Keep transformations reproducible and readable: prefer clear pandas operations over one-liners that bury what changed. Comment non-obvious mappings (e.g. the dict used for a spelling-variant merge) directly in the code so the notebook is self-documenting even without the report.
- End with a cell that re-displays value counts for each cleaned column, so the user can immediately see the before/after in the notebook itself.

## Writing the report

Create the folder `data cleaning report/` in the project root if it doesn't exist, and write `Data_Cleaning_Categorical_Columns.md` inside it. Use `references/report_template.md` as the structure — read it before writing the report. The template is organized so a reader can either skim the summary table at the top or drill into any one column's full history.

Fill it in with real evidence, not generic statements: actual value counts, actual before/after examples, and the actual reasoning discussed with the user for each judgment call. A line like "standardized formatting" with no specifics is much less useful than "trimmed whitespace and lowercased 47 values in `country`; example: `' usa '` → `'usa'`."

## Updating a previous cleaning pass

If the user comes back later and says something like "actually don't merge NY into New York" or "redo the rare-category grouping with a different threshold":

1. Read the existing report to understand what was done and why.
2. Find and edit the relevant notebook cell(s) directly — don't re-run the whole pipeline from scratch or duplicate cells, since that leaves stale cells behind and confuses the notebook's narrative. Re-run affected cells (and anything downstream that depends on them) so the notebook's outputs stay correct.
3. Update only the affected section(s) of the report to reflect the new decision — add a brief note of what changed and why (e.g., "Revised 2026-09-26: user requested 'NY' remain a distinct category rather than merging into 'New York'"), rather than rewriting the whole report from scratch.
4. Confirm with the user what changed in both places before considering the update done.

## Reference

- `references/report_template.md` — the Markdown report structure to follow when writing `Data_Cleaning_Categorical_Columns.md`.
