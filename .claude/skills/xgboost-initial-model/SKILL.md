---
name: xgboost-initial-model
description: Train a first-pass ("initial") XGBoost model for a user's ML project inside their Jupyter notebook, complete with cross-validation and a fixed set of evaluation metrics (accuracy, precision, recall, F1, ROC-AUC, PR-AUC for classification; MAE, MSE, RMSE, R², MAPE for regression), all computed via scikit-learn's cross_validate. Use this whenever the user asks to train an initial, baseline, or first XGBoost model for their project, even if they don't spell out every detail (e.g. "train an initial xgboost model", "let's get a baseline XGBoost going", "fit an XGBoost model on my data and check CV scores"). Always confirm problem type (classification vs regression), categorical-column handling, the training data to use, random state, and CV strategy with the user before running anything — this skill is a guided, confirm-as-you-go workflow, not a fire-and-forget script.
---

# Initial XGBoost Model

Train a clean, first-pass XGBoost model for the user's project, evaluate it with
cross-validation, write the working code into their notebook, and summarize
everything in an `Initial_XGBoost_Model.md` file. No hyperparameter tuning is
performed here — this is a baseline to establish that the pipeline works and to
get a first read on model performance, not a tuned final model.

The defining trait of this skill is **collaboration, not automation**. At several
points below, Claude must stop and confirm a decision with the user before writing
code. Guessing silently and only showing the result defeats the purpose — the user
wants to be in the loop on the choices that shape the model, and confirming also
catches mistakes (wrong target column, wrong split, etc.) before they get baked into
a notebook.

## Why confirm instead of just deciding

An LLM can often correctly infer whether a problem is classification or regression,
which columns are categorical, and what a sane CV setup looks like. But "often
right" is not good enough when the output is going straight into someone's project
notebook and analysis file — a wrong guess here (e.g. treating a low-cardinality
integer target as classification when it's actually a regression count, or missing
a categorical column encoded as an integer) quietly produces a misleading model.
Confirming each judgment call with the user costs one short question and removes
that risk entirely, while still letting Claude do all the actual work of detecting,
building, and writing.

## Workflow

Work through these steps in order. Each "Confirm" sub-step means: state your
finding/recommendation and ask the user to confirm or correct it before moving on.
Don't batch every question into one giant upfront interrogation — it's fine to ask
them in sequence as you reach each step, since earlier answers (like which columns
are the features) inform later questions (like which of those are categorical).

### 1. Locate the project and the notebook

Find the `.ipynb` notebook the user is working in for this project (ask if it's
ambiguous which notebook or project folder they mean). All new cells go into this
notebook via the NotebookEdit tool, appended after the existing cells. Read the
notebook first so you know what variables, imports, and data already exist —
don't duplicate imports or reload data that's already loaded.

### 2. Confirm the training data

Ask the user which variables in the notebook hold the training features and
target (e.g. `X_train`, `y_train`), and whether a held-out test/validation set
exists and what it's called. Since cross-validation is being performed on the
training set, confirm explicitly that the CV should run on the training split
named (not the full dataset and not the test set) — mixing this up silently
leaks test data into the CV estimate, which is exactly the kind of mistake this
confirmation step exists to prevent.

If the notebook doesn't already have a clear train/test split, tell the user
you don't see one and ask them to point you to it or create it first — this
skill assumes a split already exists rather than making one.

### 3. Determine and confirm the problem type

Inspect the target variable (`y_train` or whatever the user named it):
- Numeric with many unique values and continuous-looking spread → likely regression.
- Categorical dtype, small number of unique values, strings, booleans, or a
  numeric column with only a handful of distinct integer values → likely
  classification (note whether it's binary or multiclass, since that affects
  the XGBoost objective and some metrics).

State your read (e.g. "The target `churn` has 2 unique values, so this looks
like a binary classification problem") and ask the user to confirm. Some
targets are genuinely ambiguous (a low-cardinality integer could be a count
regression or an ordinal classification) — when it's unclear, say so and let
the user decide rather than picking one silently.

### 4. Detect and confirm categorical columns

Scan the feature columns for `object`, `category`, or `bool` dtypes, and flag
any numeric-looking columns that seem like they're actually encoded categories
(e.g. low-cardinality integer codes) so the user can weigh in on those too.
Present the list you found and ask the user to confirm or amend it.

If any categorical columns are confirmed, plan to pass `enable_categorical=True`
to the XGBoost constructor and make sure those columns end up as pandas
`category` dtype before fitting (XGBoost requires this even with
`enable_categorical=True` — a column left as `object` dtype will error out).
If there are no categorical columns, skip this and don't set the parameter.

Check each confirmed column's current dtype before touching it: if it's
already `category`, leave it alone — don't re-cast it. Only convert the ones
that aren't already `category` (typically `object` or `bool`). This matters
because a column that's already `category` may carry curated metadata (a
specific category ordering, or a fixed set of categories that includes ones
not present in this particular training slice) that a blanket
`astype("category")` would silently throw away and rebuild from just the
values seen in `X_train`. Re-deriving categories from a subset of the data
is also how a category present only in the test set ends up missing from the
training set's dtype — the reference script's `prepare_categoricals` helper
does this dtype check for you.

### 5. Ask about random state

Ask whether the user wants to set a `random_state` (for reproducible results)
or leave it unset. If they want one set but have no preference for the value,
a conventional default like `42` is fine — just say that's what you're using.
Use the same random state for both the XGBoost model and the CV splitter if
one is set, so the whole run is reproducible end to end.

### 6. Decide and confirm the cross-validation approach

Recommend a CV strategy based on the confirmed problem type:
- **Classification**: `StratifiedKFold` — preserves class proportions in each
  fold, which matters especially with imbalanced classes.
- **Regression**: plain `KFold`.

Recommend a fold count — 5 is a sane default for most dataset sizes; suggest
fewer (e.g. 3) for small datasets where 5 folds would leave very few samples
per fold, and mention this reasoning to the user. Ask the user to confirm the
strategy and fold count (or override them) before running anything.

### 7. Evaluation metrics (fixed set — no need to ask)

Unlike the steps above, the metrics aren't a judgment call, so there's nothing
to confirm here — always report this fixed set, matched to the confirmed
problem type. Both sets are simple scalars, so both come straight out of a
single `cross_validate` call and are reported per-fold with mean ± std — no
separate pooled-prediction step needed.

- **Classification**: Accuracy, Precision, Recall, F1-score, ROC-AUC, PR-AUC
  (average precision).
  - Binary: use the plain scorers (`precision`, `recall`, `f1`, `roc_auc`,
    `average_precision`).
  - Multiclass: Precision/Recall/F1 need an averaging strategy —  use
    macro-averaged (`precision_macro`, `recall_macro`, `f1_macro`) so
    minority classes aren't drowned out, and mention weighted-average as an
    alternative if the user cares more about overall performance than
    per-class balance. ROC-AUC needs `roc_auc_ovr`. PR-AUC doesn't have a
    built-in multiclass string scorer in scikit-learn, so build one with
    `make_scorer(average_precision_score, average="macro", needs_proba=True)`
    (or with `response_method="predict_proba"` on newer scikit-learn
    versions) so it still comes from the same `cross_validate` call rather
    than a separate code path.
  - Call out PR-AUC's importance explicitly when the classes look imbalanced,
    since ROC-AUC can look deceptively good on imbalanced data while PR-AUC
    reflects performance on the minority class more honestly.

- **Regression**: MAE, MSE, RMSE, R², and MAPE — via `neg_mean_absolute_error`,
  `neg_mean_squared_error`, `neg_root_mean_squared_error`, `r2`, and
  `neg_mean_absolute_percentage_error`. Flag it to the user if the target has
  zero or near-zero values, since MAPE is unstable (or undefined) in that
  case, but still report it.

### 8. Build and run

Once problem type, categorical handling, random state, training data, and CV
approach are confirmed (metrics are fixed — see step 7), write the actual
working code. Use `scripts/train_initial_xgboost.py` as the reference
implementation — it implements this exact workflow (model setup, categorical
casting, a single `cross_validate` call with the full scoring dict, formatted
summary) so you're not reinventing the metric-collection logic by hand each
time. Adapt the specific pieces (feature/target variable names, problem type
branch, CV strategy) to what was confirmed with the user, then translate it
into notebook cells using the notebook's existing variable names.

Use `xgboost.XGBClassifier` for classification problems and
`xgboost.XGBRegressor` for regression problems.

Add the code as one or more new cells at the end of the notebook via
NotebookEdit, in a logical order (imports/setup → categorical casting if
needed → model + CV setup → run CV → print/display results). Keep cells
focused — don't cram the entire workflow into a single giant cell if it reads
more clearly split up, since the user will be reading and re-running this
notebook later.

Actually execute the cells (or ask the user to, if you don't have kernel
execution access in this environment) so the metrics in the `.md` summary
reflect real output rather than a guess.

### 9. Write `Initial_XGBoost_Model.md`

Create this file in the project folder (the same folder the notebook lives
in, unless the user says otherwise). Include:

- **Date** the model was trained
- **Problem type** (classification/regression, and binary/multiclass if
  applicable), as confirmed with the user
- **Training data used** — the variable names and shape (rows × columns) of
  the training set the CV was run on
- **Target column**
- **Categorical columns** — the confirmed list, or "None" if there were none
- **Random state** — the value used, or "Not set" if the user chose not to
  set one
- **Cross-validation setup** — strategy (KFold/StratifiedKFold) and number of
  folds, as confirmed
- **Metrics** (all per-fold, mean ± std):
  - Classification: accuracy, precision, recall, F1-score, ROC-AUC, PR-AUC
  - Regression: MAE, MSE, RMSE, R², MAPE
- **Notes** — explicitly state that no hyperparameter tuning was performed,
  since this is a baseline model; XGBoost's own defaults were used aside from
  `random_state`/`enable_categorical` as applicable

Keep the file plain and scannable — headings and a metrics table read better
here than dense prose, since the user (or a teammate) will likely skim this
later to recall what the baseline was.

## After finishing

Give the user a short summary of the headline results (e.g. "Baseline XGBoost
classifier: mean ROC-AUC 0.87 ± 0.02 across 5 folds") and point them to the
notebook cells and the `Initial_XGBoost_Model.md` file. Since no tuning was
done, it's worth noting this is a starting point and asking if they want to
move on to hyperparameter tuning or feature engineering next — but don't do
either of those unprompted, since they're outside this skill's scope.
