---
name: basic-data-exploration
description: Adds a standard *basic* data exploration block to a Jupyter notebook — loading the data into a pandas DataFrame and running .info(), .head(), .describe() (numerical and categorical), missing-value checks (counts, percentages, heatmap), and duplicate-row checks, each with its own markdown header and code cell. Make sure to use this skill whenever the user asks to do "basic data exploration", "initial data exploration", "quick look at the data", or wants the first step of an ML/data-science pipeline set up in a notebook. This is deliberately limited to the basic/first-pass checks above — do NOT use this for deeper or more advanced exploratory data analysis (EDA), feature analysis, correlation studies, or visualization work beyond the fixed list here; that is handled by a separate, more advanced skill. Only for .ipynb notebooks; not for standalone scripts, reports, or non-notebook analysis.
---

# Basic Data Exploration Notebook Starter

Appends a fixed, first-step *basic* data exploration block to a project's Jupyter notebook: load the data, inspect it, describe it, and check data quality (missing values, duplicates) — with clean markdown section headers between each code cell.

This is intentionally scoped to basic checks only. A separate skill handles deeper/advanced EDA (correlation analysis, distribution plots, feature relationships, etc.) — don't expand this skill's scope to cover that; point the user to the other skill instead if they ask for more than the basics.

## When to use this

Trigger this skill when the user wants to:
- Kick off **basic** or **initial** data exploration on a dataset
- Add the first step of an ML pipeline to a notebook
- Get a "quick look" at a dataset's shape, types, and data-quality issues

Do **not** trigger this for requests about deeper/advanced EDA, correlation, feature engineering, or custom visualizations — those belong to the separate advanced-EDA skill.

## Workflow

### 1. Locate the notebook and the data file

Do **not** guess or search silently. If the user hasn't already given you both paths in this conversation:
- Ask for the path to the project notebook (`.ipynb`). If it doesn't exist yet, that's fine — the script creates it.
- Ask for the path to the data file (csv, tsv, xlsx, xls, json, parquet, or feather).

If the user already stated both paths earlier in the conversation, don't ask again — just confirm your understanding briefly if there's any ambiguity (e.g. multiple data files mentioned).

### 2. Make sure `nbformat` is available

```bash
pip install nbformat --break-system-packages
```

(It's usually already installed; the install is a fast no-op if so.)

### 3. Run the cell-insertion script

```bash
python3 scripts/add_eda_cells.py <notebook_path> <data_path> [--df-name df]
```

**If the notebook already has a basic exploration block in it**, the script will detect that (it looks for a `## Data Exploration` markdown header) and refuse to add a second one — it exits without changing the file and prints `ALREADY_EXISTS`. When you see that:

- **Stop. Do not automatically re-run with `--force`.**
- Tell the user basic exploration already appears to be done in this notebook, and ask whether they want you to add another block anyway (e.g. because the data changed, or they want a fresh copy), skip it, or do something else instead.
- Only re-run with `--force` if the user explicitly confirms they want it added again:
  ```bash
  python3 scripts/add_eda_cells.py <notebook_path> <data_path> --force
  ```

If the script succeeds normally (no `ALREADY_EXISTS`), it appends the following markdown + code cells to the end of the notebook:

1. `## Data Exploration` header
2. Imports (`pandas`, `numpy`, `matplotlib.pyplot`, `seaborn`)
3. A `load_data(path)` helper function, and a call to it. This is generic by construction, not by a hardcoded list: it tries pandas' readers (Excel, JSON, Parquet, Feather, and delimited text) in an order guided lightly by the extension, and for delimited text it uses pandas' own `sep=None, engine='python'` sniffing — which detects whatever separator the file actually uses on its own. If the extension-guided reader fails, it falls through the rest until one works, and only raises if none do (with a clear message listing what was tried). This means it isn't limited to any specific set of formats or separators anticipated in advance.
4. `.info()`
5. `.head()`
6. `.describe()` for numerical features
7. `.describe()` for categorical features (only the `object`/`category` columns; prints a message if none exist)
8. Missing values: a summary table of count + percentage missing per column (only columns with at least one missing value), plus a `seaborn` heatmap of the missing-value pattern
9. Duplicate rows: a count, and if any exist, the duplicate rows themselves

Use `--df-name` if the user wants a DataFrame variable name other than `df` (e.g. to match an existing naming convention in their notebook).

### 4. Verify the notebook is valid

After running the script (and only if it actually made changes), sanity-check the notebook parses and — when a kernel with the needed packages is available — actually executes cleanly:

```bash
jupyter nbconvert --to notebook --execute <notebook_path> --output <notebook_path>
```

Skip execution (but still mention it to the user) if the data file can't actually be read in this environment (e.g. it lives somewhere only the user's machine can access) — in that case just confirm the notebook JSON is well-formed instead:

```bash
python3 -c "import nbformat; nbformat.read('<notebook_path>', as_version=4)"
```

### 5. Report back to the user

Tell the user what was added (the list of sections above, briefly) and where the notebook lives. If you executed it, mention that it ran cleanly, or flag anything that failed so they can fix it (e.g. wrong column assumptions, missing package). Remind them this is step one of the pipeline — later steps (cleaning, feature engineering, deeper EDA, modeling, etc.) can build on this same notebook.

## Notes

- This skill only **appends** cells — it never deletes or modifies existing cells.
- It refuses to add a second basic-exploration block silently — always check with the user first if `ALREADY_EXISTS` comes back (see step 3).
- **Loading is format- and separator-agnostic by design, not by lookup table.** The generated `load_data` helper tries pandas' own readers in turn and uses pandas' built-in delimiter sniffing (`sep=None, engine='python'`) for text files, so it isn't limited to a fixed set of extensions or separators anticipated in advance — comma, semicolon, tab, pipe, whitespace, an unfamiliar extension that's secretly CSV, a file with no extension at all, etc. all work the same way. You shouldn't need to ask the user what separator or format their file uses.
- If a file genuinely can't be loaded by any of the readers tried, `load_data` raises a `ValueError` listing every reader it attempted and why each failed — read that error rather than guessing further.
- If the user wants a different set of exploration steps than this fixed set (e.g. no heatmap, or additional plots), edit the generated cells directly in the notebook after running the script, rather than modifying the script's defaults — this keeps the skill's output predictable across runs. For genuinely deeper exploration, defer to the separate advanced-EDA skill instead.
