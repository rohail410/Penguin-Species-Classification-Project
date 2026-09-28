"""
Reference implementation for the xgboost-initial-model skill.

This is NOT meant to be run as-is against a real project. It's a template
Claude should read and adapt when writing notebook cells for the user: swap
in the confirmed variable names, problem-type branch, categorical columns,
and CV strategy. The metric set itself is fixed (not a judgment call), so
it's implemented in full here rather than left as a placeholder — every
invocation of the skill should report the same metrics.

All metrics here are simple scalars, so all of them come from a single
`cross_validate` call and are reported per-fold with mean ± std. There's no
separate pooled-prediction step — that was useful for things like a
confusion matrix (which isn't a scalar and doesn't average sensibly across
folds), but this skill sticks to scalar metrics, so one cross_validate call
per problem type covers everything.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold, cross_validate
from sklearn.metrics import average_precision_score, make_scorer

# ---------------------------------------------------------------------------
# Placeholders — replace these with the confirmed values before adapting the
# code below into notebook cells. Everything in this section should come
# from what the user confirmed, not from a silent guess.
# ---------------------------------------------------------------------------
X_train = None            # confirmed training features (DataFrame)
y_train = None            # confirmed training target (Series/array)
CATEGORICAL_COLUMNS = []  # confirmed list of categorical column names, or []
RANDOM_STATE = 42         # confirmed value, or None if the user opted out
N_FOLDS = 5               # confirmed fold count
PROBLEM_TYPE = "classification"  # "classification" or "regression", confirmed
IS_BINARY = True          # only relevant if PROBLEM_TYPE == "classification"


# ---------------------------------------------------------------------------
# Step: cast confirmed categorical columns to pandas 'category' dtype.
# XGBoost requires this even with enable_categorical=True — an 'object'
# dtype column will raise an error at fit time.
#
# Columns already in 'category' dtype are left untouched rather than
# re-cast. A blanket astype("category") on an already-categorical column
# would silently rebuild its categories from just the values present in
# this DataFrame, discarding any curated ordering or a fixed category set
# that intentionally includes values not seen in this particular slice
# (e.g. a category that only shows up in the test set).
# ---------------------------------------------------------------------------
def prepare_categoricals(df: pd.DataFrame, categorical_columns: list) -> pd.DataFrame:
    df = df.copy()
    for col in categorical_columns:
        if isinstance(df[col].dtype, pd.CategoricalDtype):
            continue  # already category dtype — don't touch it
        df[col] = df[col].astype("category")
    return df


if CATEGORICAL_COLUMNS:
    X_train = prepare_categoricals(X_train, CATEGORICAL_COLUMNS)

enable_categorical = bool(CATEGORICAL_COLUMNS)


# ---------------------------------------------------------------------------
# Step: build the model, CV splitter, and scoring dict for the confirmed
# problem type.
# ---------------------------------------------------------------------------
if PROBLEM_TYPE == "classification":
    from xgboost import XGBClassifier

    model = XGBClassifier(
        random_state=RANDOM_STATE,
        enable_categorical=enable_categorical,
    )
    cv = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    if IS_BINARY:
        scoring = {
            "accuracy": "accuracy",
            "precision": "precision",
            "recall": "recall",
            "f1": "f1",
            "roc_auc": "roc_auc",
            "pr_auc": "average_precision",
        }
    else:
        # Multiclass: precision/recall/f1 need an averaging strategy (macro
        # keeps minority classes from being drowned out — swap for the
        # "_weighted" variants if overall performance matters more than
        # per-class balance). ROC-AUC needs one-vs-rest. PR-AUC has no
        # built-in multiclass string scorer in scikit-learn, so it's built
        # manually with make_scorer so it still comes from this same
        # cross_validate call.
        pr_auc_macro_scorer = make_scorer(
            average_precision_score, average="macro", response_method="predict_proba"
        )
        scoring = {
            "accuracy": "accuracy",
            "precision_macro": "precision_macro",
            "recall_macro": "recall_macro",
            "f1_macro": "f1_macro",
            "roc_auc": "roc_auc_ovr",
            "pr_auc_macro": pr_auc_macro_scorer,
        }

elif PROBLEM_TYPE == "regression":
    from xgboost import XGBRegressor

    model = XGBRegressor(
        random_state=RANDOM_STATE,
        enable_categorical=enable_categorical,
    )
    cv = KFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    scoring = {
        "mae": "neg_mean_absolute_error",
        "mse": "neg_mean_squared_error",
        "rmse": "neg_root_mean_squared_error",
        "r2": "r2",
        "mape": "neg_mean_absolute_percentage_error",
    }
    # sklearn reports these as negative numbers (its convention so "higher
    # is always better" internally) — flip the sign back for a readable
    # table below.
    NEGATED_METRICS = {"mae", "mse", "rmse", "mape"}

else:
    raise ValueError(f"Unknown PROBLEM_TYPE: {PROBLEM_TYPE!r}")


# ---------------------------------------------------------------------------
# Step: run cross-validation once with the full scoring dict.
# ---------------------------------------------------------------------------
cv_results = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring)


# ---------------------------------------------------------------------------
# Step: summarize per-fold scores and mean ± std for each metric.
# ---------------------------------------------------------------------------
def summarize_cv_results(cv_results: dict, scoring: dict, negated_metrics: set = frozenset()) -> pd.DataFrame:
    rows = []
    for metric_name in scoring:
        scores = cv_results[f"test_{metric_name}"]
        if metric_name in negated_metrics:
            scores = -scores
        rows.append(
            {
                "metric": metric_name,
                "fold_scores": np.round(scores, 4).tolist(),
                "mean": round(scores.mean(), 4),
                "std": round(scores.std(), 4),
            }
        )
    return pd.DataFrame(rows)


negated = NEGATED_METRICS if PROBLEM_TYPE == "regression" else set()
summary_df = summarize_cv_results(cv_results, scoring, negated)
print("Per-fold metrics (mean ± std):")
print(summary_df.to_string(index=False))


# ---------------------------------------------------------------------------
# Step: fit the final model on the full training set (not just one fold) so
# it's available in the notebook for the user's next steps (e.g. checking
# feature importances, predicting on a held-out test set).
# ---------------------------------------------------------------------------
model.fit(X_train, y_train)
