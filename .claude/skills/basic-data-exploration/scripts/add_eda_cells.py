#!/usr/bin/env python3
"""
Append a standard basic-data-exploration block to a Jupyter notebook.

Adds, in order, markdown + code cells for:
  - Imports
  - Loading the data file into a pandas DataFrame (format- and
    separator-agnostic — see load_data() below)
  - .info()
  - .head()
  - .describe() for numerical features
  - .describe() for categorical features
  - Missing value counts, percentages, and a heatmap
  - Duplicate row check

Usage:
    python add_eda_cells.py <notebook_path> <data_path> [--df-name df]

If <notebook_path> does not exist, a new empty notebook is created there.
Cells are always appended to the end of the notebook (never overwrites
existing cells), so this is safe to run on a notebook that already has
other work in it.
"""

import argparse
import sys
from pathlib import Path

try:
    import nbformat
    from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
except ImportError:
    print("ERROR: nbformat is required. Install it with:")
    print("  pip install nbformat --break-system-packages")
    sys.exit(1)


HEADER_MARKER = "## Data Exploration"


def already_has_exploration(nb) -> bool:
    """Return True if the notebook already contains a basic-exploration block."""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown" and HEADER_MARKER in cell.get("source", ""):
            return True
    return False


# This is the actual fix for "it only worked for comma-separated .csv files":
# rather than the *script* guessing a format/separator from the file extension
# and baking one hardcoded choice into the notebook, we generate a small
# loader function that lives IN the notebook and tries several of pandas'
# own readers at run time, falling through to the next on failure. The
# delimited-text branch uses pandas' own `sep=None, engine="python"` sniffing
# (which detects comma, semicolon, tab, pipe, whitespace, etc. on its own —
# nothing here hardcodes a specific separator or a fixed list of formats),
# so it isn't limited to whatever formats/separators we happened to think of.
LOAD_DATA_HELPER = '''\
def load_data(path):
    """
    Load a tabular data file into a pandas DataFrame without assuming its
    format or, for delimited text, its separator. Tries readers roughly in
    order of what the extension suggests, then falls through the rest —
    including generic delimiter sniffing — until one works.
    """
    import pandas as pd
    from pathlib import Path

    ext = Path(path).suffix.lower()

    def read_delimited(p):
        # sep=None + engine="python" makes pandas sniff the actual delimiter
        # (comma, semicolon, tab, pipe, whitespace, ...) from the file itself.
        return pd.read_csv(p, sep=None, engine="python")

    candidates = {
        "excel": lambda p: pd.read_excel(p),
        "json": lambda p: pd.read_json(p),
        "parquet": lambda p: pd.read_parquet(p),
        "feather": lambda p: pd.read_feather(p),
        "delimited": read_delimited,
    }

    ext_hint = {
        ".xlsx": "excel", ".xls": "excel", ".xlsm": "excel",
        ".json": "json",
        ".parquet": "parquet",
        ".feather": "feather",
    }.get(ext, "delimited")

    order = [ext_hint] + [k for k in candidates if k != ext_hint]

    errors = {}
    for key in order:
        try:
            df = candidates[key](path)
            if key != ext_hint:
                print(f"Note: '{ext}' didn't load as expected; loaded successfully as {key} instead.")
            return df
        except Exception as e:
            errors[key] = e

    raise ValueError(
        f"Could not load {path!r} with any known reader. Tried: "
        + ", ".join(f"{k} ({e.__class__.__name__})" for k, e in errors.items())
    )
'''


def build_cells(data_path: str, df_name: str):
    cells = []

    cells.append(new_markdown_cell("## Data Exploration"))

    cells.append(new_code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n\n"
        "pd.set_option('display.max_columns', None)"
    ))

    cells.append(new_markdown_cell(
        "### Load Data\n"
        "`load_data` figures out the file format and, for delimited text, the "
        "separator, on its own — no assumptions are hardcoded here."
    ))
    cells.append(new_code_cell(LOAD_DATA_HELPER))
    cells.append(new_code_cell(f"{df_name} = load_data({data_path!r})\n{df_name}.shape"))

    cells.append(new_markdown_cell("### Initial Inspection"))
    cells.append(new_code_cell(f"{df_name}.info()"))
    cells.append(new_code_cell(f"{df_name}.head()"))

    cells.append(new_markdown_cell("### Descriptive Statistics — Numerical Features"))
    cells.append(new_code_cell(f"{df_name}.describe()"))

    cells.append(new_markdown_cell("### Descriptive Statistics — Categorical Features"))
    cells.append(new_code_cell(
        f"cat_cols = {df_name}.select_dtypes(include=['object', 'category']).columns\n"
        f"if len(cat_cols) > 0:\n"
        f"    display({df_name}[cat_cols].describe())\n"
        f"else:\n"
        f"    print('No categorical columns detected.')"
    ))

    cells.append(new_markdown_cell("### Missing Values"))
    cells.append(new_code_cell(
        f"missing_count = {df_name}.isnull().sum()\n"
        f"missing_pct = (missing_count / len({df_name})) * 100\n"
        f"missing_summary = pd.DataFrame({{'missing_count': missing_count, 'missing_pct': missing_pct}})\n"
        f"missing_summary = missing_summary[missing_summary['missing_count'] > 0].sort_values('missing_count', ascending=False)\n"
        f"missing_summary"
    ))
    cells.append(new_code_cell(
        f"plt.figure(figsize=(10, 6))\n"
        f"sns.heatmap({df_name}.isnull(), cbar=False, yticklabels=False, cmap='viridis')\n"
        f"plt.title('Missing Values Heatmap')\n"
        f"plt.tight_layout()\n"
        f"plt.show()"
    ))

    cells.append(new_markdown_cell("### Duplicate Rows"))
    cells.append(new_code_cell(
        f"dup_count = {df_name}.duplicated().sum()\n"
        f"print(f'Number of duplicate rows: {{dup_count}}')\n"
        f"if dup_count > 0:\n"
        f"    display({df_name}[{df_name}.duplicated(keep=False)].sort_values(by={df_name}.columns.tolist()[0]))"
    ))

    return cells


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook_path", help="Path to the .ipynb file (created if missing)")
    parser.add_argument("data_path", help="Path to the data file to load (any pandas-readable tabular format)")
    parser.add_argument("--df-name", default="df", help="Variable name for the DataFrame (default: df)")
    parser.add_argument("--force", action="store_true",
                         help="Add the block even if one already exists in the notebook")
    args = parser.parse_args()

    nb_path = Path(args.notebook_path)

    if nb_path.exists():
        nb = nbformat.read(nb_path, as_version=4)
    else:
        nb = new_notebook()
        nb_path.parent.mkdir(parents=True, exist_ok=True)

    if already_has_exploration(nb) and not args.force:
        print("ALREADY_EXISTS: This notebook already has a '## Data Exploration' block.")
        print("No changes made. Re-run with --force to add another block anyway.")
        sys.exit(2)

    new_cells = build_cells(args.data_path, args.df_name)
    nb["cells"].extend(new_cells)

    nbformat.write(nb, nb_path)
    print(f"Added {len(new_cells)} cells to {nb_path}")


if __name__ == "__main__":
    main()
