# Initial XGBoost Model

- **Date trained:** 2026-09-29
- **Problem type:** Multiclass classification (3 classes: Adelie=0, Chinstrap=1, Gentoo=2)
- **Training data:** `X_train` (800 × 6), `y_train` (800,) — the 80% stratified training split; the test set (`X_test`, `y_test`) was not used
- **Target column:** `species` (label-encoded)
- **Categorical columns:** `island`, `sex` (already `category` dtype; `enable_categorical=True`)
- **Random state:** 42 (model and CV splitter)
- **Cross-validation:** `StratifiedKFold`, 5 folds, shuffled

## Metrics (5-fold CV, mean ± std)

| Metric | Mean | Std | Per-fold |
|---|---|---|---|
| Accuracy | 0.9862 | 0.0083 | 0.975, 0.9875, 0.9875, 0.9812, 1.0 |
| Precision (macro) | 0.9866 | 0.0093 | 0.972, 0.9872, 0.9912, 0.9826, 1.0 |
| Recall (macro) | 0.9855 | 0.0079 | 0.9782, 0.9872, 0.9833, 0.9788, 1.0 |
| F1 (macro) | 0.9859 | 0.0084 | 0.9749, 0.9872, 0.987, 0.9806, 1.0 |
| ROC-AUC (OvR) | 0.9975 | 0.0031 | 0.9958, 0.9999, 0.9998, 0.9921, 1.0 |
| PR-AUC (macro) | 0.9963 | 0.0042 | 0.9917, 0.9997, 0.9995, 0.9906, 1.0 |

## Notes

- Baseline only: **no hyperparameter tuning** was performed. XGBoost defaults were used apart from `random_state=42` and `enable_categorical=True`.
- Missing values (~1% per column) were left as `NaN`; XGBoost handles them natively.
- Chinstrap is the smallest class, so macro-averaged precision/recall/F1 and PR-AUC are the more informative metrics.
- The final model was fit on the full training set in the notebook (`model`).
