---
name: notebook-eda
description: >
  Run a full exploratory data analysis (EDA) on a pandas DataFrame inside a Jupyter notebook and add the
  results as new cells in that same notebook. Use whenever the user asks to "do EDA", "explore the data",
  "analyze this dataframe", or similar, in a notebook with a pandas DataFrame already loaded. Covers -
  an fg-data-profiling report saved to an "EDA report" folder (asking before overwriting an existing one),
  one combined per-feature panel for numerical features (boxplot + histogram faceted by target class,
  stacked in the same column), and one combined per-feature panel for categorical features (countplot
  stacked above a row-normalized percentage crosstab heatmap vs a categorical target). Always use this
  for dataframe EDA requests in a notebook, even if the user just says "explore this" without listing
  specific plots — this skill defines exactly which plots/report to produce and how to lay out the new
  EDA section.
---

# Notebook EDA

Adds a complete EDA section to the user's notebook for a pandas DataFrame already in memory: an `fg-data-profiling` report, plus a set of matplotlib/seaborn plots relating every feature to a target column. Everything below is added to the notebook as real cells (markdown headers + executed code cells) — this is not a script run outside the notebook, and it does not just describe what to do.

## 0. Before starting

Confirm the essentials rather than guessing silently:

1. **Which DataFrame?** If exactly one pandas DataFrame variable exists in the notebook's namespace, use it. If there are several, ask the user which one.
2. **Which column is the target?** Never assume (e.g. never assume it's the last column). Ask the user for the target column name unless they already named it in their request.
3. **Dependencies.** Confirm `fg-data-profiling`, `pandas`, `matplotlib`, and `seaborn` are installed in the notebook's kernel; if not, add a setup cell that installs them (`%pip install fg-data-profiling seaborn` — pandas/matplotlib are normally already present).

`fg-data-profiling` is the current name of what used to be `pandas-profiling` / `ydata-profiling` (same project, renamed). The import path is still the original one:

```python
from data_profiling import ProfileReport
```

Do not `pip install ydata-profiling` or `pandas-profiling` — install `fg-data-profiling` and import from `data_profiling`.

## 1. Classify the columns

Split the DataFrame's columns (excluding the target) into **numerical** and **categorical** using dtype as the default rule:

- `int64` / `float64` (and other numeric dtypes) → numerical
- `object`, `category`, `bool` → categorical

For any column that doesn't cleanly fit this — e.g. a numeric column with very few unique values that's really a discrete/categorical code (a common example: a 0/1 flag stored as `int64`), a `datetime` column, or an ID-like column with near-unique values — **don't decide silently**. Point out the ambiguous column(s) to the user and ask how to classify them before proceeding. A reasonable trigger for "ambiguous": a numeric column with fewer than ~15 unique values, or a unique-value count within a couple of the row count (likely an identifier, which should probably be excluded from plotting entirely — ask).

Also determine the target's own type (numerical vs categorical) the same way, since it decides which plots in Section 3 apply.

## 2. Generate the fg-data-profiling report

1. Compute the report folder path as `EDA report` inside the notebook's working directory.
2. If `EDA report/` does not exist, create it.
3. If it already exists, **ask the user whether to overwrite it** before writing anything into it. If they say no, pick a non-clobbering alternative (e.g. ask for a different folder name, or skip regenerating the report and only add the new plots) — don't silently rename or skip.
4. Add a code cell that builds and saves the report:

```python
from pathlib import Path
from data_profiling import ProfileReport

report_dir = Path("EDA report")
report_dir.mkdir(parents=True, exist_ok=True)

profile = ProfileReport(df, title="EDA Report")
profile.to_file(report_dir / "eda_report.html")
profile.to_notebook_iframe()
```

Calling `.to_notebook_iframe()` also renders the report inline in the notebook right after the cell — keep that call so the user sees it immediately, not just a saved file.

## 3. Per-feature plots against the target

Add a markdown cell `## Exploratory Data Analysis` to start the section, then subsections as below. Every plot must both **render inline** in the notebook and be **saved as an image file** into `EDA report/` (create an `EDA report/plots/` subfolder for these so they don't clutter the top level). Use a helper so every plotting cell follows the same pattern:

```python
import matplotlib.pyplot as plt
import seaborn as sns

plot_dir = report_dir / "plots"
plot_dir.mkdir(parents=True, exist_ok=True)

def save_and_show(fig, name):
    fig.savefig(plot_dir / name, bbox_inches="tight", dpi=150)
    plt.show()
```

### 3a. Numerical features → one combined panel per feature, faceted by target class

For **each** numerical feature, produce a **single figure** laid out as a grid with one column per target class and two rows: boxplot on top, histogram on bottom — so the boxplot and histogram for a given class stack in the same column. This replaces the older approach of one boxplot with all classes as different boxes in a single axes, and one histogram with all classes overlaid via `hue` — those are now split into per-class panels instead.

```python
classes = sorted(df[target_col].dropna().unique())

for col in numerical_cols:
    n = len(classes)
    fig, axes = plt.subplots(2, n, figsize=(4 * n, 8), sharex="row", sharey="row")
    if n == 1:
        axes = axes.reshape(2, 1)  # keep 2D indexing consistent for a single-class edge case

    for j, cls in enumerate(classes):
        subset = df.loc[df[target_col] == cls, col]

        sns.boxplot(y=subset, ax=axes[0, j])
        axes[0, j].set_title(f"{target_col} = {cls}")
        axes[0, j].set_xlabel("")

        sns.histplot(subset, kde=True, ax=axes[1, j])
        axes[1, j].set_xlabel(col)

    fig.suptitle(f"{col} by {target_col}")
    fig.tight_layout()
    save_and_show(fig, f"{col}_by_{target_col}.png")
```

`sharex="row"` / `sharey="row"` keep each row's axes aligned across classes so the panels are actually comparable (same value range per row).

This assumes a categorical target (one column of panels per class). If the target turns out to be numerical instead, ask the user how they'd like this section adapted (e.g. a scatterplot of feature vs. target instead of faceted boxplots/histograms) rather than silently forcing this layout onto a continuous target.

Put each feature's combined figure under its own small markdown subheading (`#### {col}`) so the notebook stays readable for datasets with many columns.

### 3b. Categorical features → one combined panel per feature (countplot + crosstab heatmap, stacked)

For each categorical feature (and any numeric-but-discrete columns identified in Section 1), produce a **single figure** with two rows: the countplot on top, the row-normalized crosstab heatmap directly below it.

```python
for col in categorical_cols:  # include discrete numeric cols classified as categorical
    target_is_categorical = ...  # from Section 1's classification of target_col

    if target_is_categorical:
        fig, axes = plt.subplots(2, 1, figsize=(7, 9))
    else:
        fig, axes = plt.subplots(1, 1, figsize=(7, 4.5))
        axes = [axes]

    sns.countplot(data=df, x=col, hue=target_col, ax=axes[0])
    axes[0].set_title(f"{col} counts by {target_col}")
    axes[0].tick_params(axis="x", rotation=45)

    if target_is_categorical:
        ct = pd.crosstab(df[col], df[target_col], normalize="index") * 100
        sns.heatmap(ct, annot=True, fmt=".1f", cmap="Blues",
                    cbar_kws={"label": "% of row"}, ax=axes[1])
        axes[1].set_title(f"{col} vs {target_col} (row-normalized %)")
        axes[1].set_ylabel(col)

    fig.tight_layout()
    save_and_show(fig, f"{col}_panel.png")
```

`normalize="index"` row-normalizes the crosstab: each row (feature category) sums to 100%, showing the target-class distribution within that feature category. `annot=True, fmt=".1f"` displays the percentages inside each cell.

The heatmap row only applies when the target is categorical (a percentage-of-target-class breakdown needs discrete target classes). If the target is numerical, the panel drops to just the countplot and a markdown note should say why the heatmap was skipped — don't silently omit it with no explanation.

## 4. Wrap-up

After all cells are added and executed, briefly summarize in chat what was created (report path, number of plots, where images were saved) — don't repeat every plot's content, the notebook already shows it.
