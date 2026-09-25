---
name: dataset-feature-description
description: >
  Explores a project's dataset and writes a Feature_Description.md documenting every column/feature — its name, a brief description of what it represents, its data type, example values, and any data quality issues (missing values, outliers, mismatched/mixed types, duplicates, inconsistent formatting, etc). Use this skill whenever the user asks to "describe the features" of a dataset, "document the columns", "profile the data", "explain the dataset", or asks for a data dictionary, feature description, or data profiling report for a project's dataset — even if they don't use the exact word "features". Trigger for any tabular data file, such as CSV, Excel (.xlsx/.xls), JSON, Parquet, or TSV.
---

# Dataset Feature Description

Explore a dataset and produce a `Feature_Description.md` file documenting every feature (column): its name, a brief description of what it represents, inferred data type, representative example values, and any data quality issues worth flagging.

## Workflow

### Step 1: Find the dataset

Look for an obvious tabular data file in the project/uploads context (CSV, XLSX/XLS, JSON, Parquet, TSV, etc.).

- If exactly one plausible dataset file is present, use it.
- If it's ambiguous (multiple candidate files, or none visible), **ask the user which file to use** rather than guessing. Don't silently pick one.
- If the user gives a path directly, use that.

### Step 2: Load the dataset

Use Python (pandas) in the bash tool to load the file based on its extension:

```python
import pandas as pd

# csv/tsv
df = pd.read_csv(path)  # sep="\t" for tsv

# excel
df = pd.read_excel(path, sheet_name=None)  # dict of all sheets if multiple

# json
df = pd.read_json(path)  # or pd.json_normalize for nested json

# parquet
df = pd.read_parquet(path)
```

If the file has multiple sheets (Excel) or is clearly multiple logical tables, handle each one separately and give each its own section in the output (or a separate report per table, using judgment — ask the user only if it's genuinely unclear which they want).

Print `df.shape`, `df.dtypes`, and `df.head()` first to get oriented before going column-by-column.

### Step 3: Explore each feature (column)

For every column, gather:

1. **Name** — the column name as-is.
2. **Description** — a brief (one sentence) explanation of what the column represents. Infer this from the column name together with its actual values (e.g. a column named `dob` full of dates in the past is "the customer's date of birth"). Don't guess wildly — if a column's name is cryptic and its values don't clarify it, say plainly that its meaning is unclear rather than inventing a plausible-sounding explanation.
3. **Type** — inferred data type. Don't just paste the pandas dtype (e.g. `object`) — figure out the *semantic* type: integer, float, categorical, boolean, datetime, free text, identifier/ID, etc.
4. **Example values** — 3–5 representative real values from the column (prefer values that show the range/variety, not just the first few rows).
5. **Data Quality Issues** — use judgment; there's no fixed checklist, but look out for things like:
   - Missing values (nulls, empty strings, placeholder strings like `"N/A"`, `"-"`, `"unknown"`)
   - Outliers or implausible values (negative ages, dates in the future/far past, prices of 0 or negative)
   - Mismatched/mixed types within a column (numbers stored as strings, inconsistent casing/formatting)
   - Duplicated rows or a column that should be unique but isn't
   - Inconsistent categories (e.g. `"USA"`, `"U.S.A"`, `"United States"` all meaning the same thing)
   - Suspicious constants (a column that's the same value for every row)
   - Anything else that would surprise someone using this data

If a column has no data quality issues, say so briefly rather than omitting the field — it's useful to know it was checked.

Useful pandas snippets for this step:

```python
col.dtype
col.isna().sum()
col.nunique()
col.value_counts().head(10)
col.describe()  # numeric columns: min/max/mean etc. — good for spotting outliers
col.sample(5)   # example values
```

Do this exploration programmatically (write a small script that loops over columns and prints summary stats) rather than eyeballing `df.head()` alone — data quality issues are often invisible in the first few rows.

### Step 4: Write Feature_Description.md

Structure the file like this:

```markdown
# Feature Description: <dataset name>

Dataset shape: <N rows> x <M columns>

## <column_name_1>
- **Description:** <brief, one-sentence explanation of what this column represents>
- **Type:** <semantic type>
- **Examples:** value1, value2, value3
- **Data Quality Issues:** <description, or "None observed">

## <column_name_2>
...
```

A summary table at the top (name | type | % missing | notes) is a nice addition for larger datasets, but the detailed per-column sections below it are the core deliverable — don't replace them with just the table.

Save the file as `Feature_Description.md` **in the project's main/root folder** — not inside the dataset's own subfolder, and not in any other nested location. Datasets often live in a `data/` (or similarly named) subfolder within a project; in that case, the report still goes in the project root, one level up from the data folder, not next to the raw file itself. If the "project root" isn't obvious from context, ask the user rather than guessing. Then present it to the user with `present_files` so they can view/download it from the chat too.

### Step 5: Note anything that needs the user's attention

After presenting the file, call out in the chat (briefly, not duplicating the doc) anything that seems important enough that the user might want to act on it immediately — e.g. a column that's entirely null, or a likely duplicate ID column.

## Notes

- If the dataset is very wide (50+ columns), still document every column — don't truncate the report. Consider grouping similar columns (e.g. a block of one-hot encoded columns) into a shared section if writing one identical entry per column would be pure repetition, but say explicitly that's what you did.
- If a column is clearly a free-text field (e.g. reviews, descriptions), don't try to enumerate its values — describe its nature, typical length, and language/content instead.
