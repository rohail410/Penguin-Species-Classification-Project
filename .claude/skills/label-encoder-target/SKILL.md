---
name: label-encoder-target
description: Encode the target (label) column of a dataset in a Jupyter notebook with scikit-learn's LabelEncoder, and convert encoded labels back to the original labels with inverse_transform. Explores the notebook to find the target, confirms it with the user, fits on the training target only, transforms the test and validation targets, and overwrites each target in the same variable. Adds the cells directly to the notebook. Use whenever the user asks to use LabelEncoder, label-encode or encode the target/label/y column, convert class labels to numbers for a classifier, or convert encoded labels or predictions back to the original labels (inverse_transform, decode labels), even if they don't say "LabelEncoder" explicitly.
---

# Label-encode the target column in a notebook

This skill does two jobs, both by adding cells to the user's notebook:

1. **Encode** the target column with `LabelEncoder` (fit on train, transform the rest).
2. **Decode** encoded labels back to the original labels with `inverse_transform`, when the user asks.

`LabelEncoder` is designed for target labels, not input features. If the user asks to label-encode feature columns, say so briefly and suggest `OrdinalEncoder` or one-hot encoding for features. Encode the target if they still want it.

## Part 1: Encode the target

### 1. Explore the notebook first

Read the notebook (`Read` on the `.ipynb` works and returns cells with outputs) before asking anything. You are looking for:

- **Candidate target columns.** Look at how the data is split and what the model is fit on: `y = df['...']`, `X, y = ...`, `train_test_split(...)`, `model.fit(X_train, y_train)`, column names like `target`, `label`, `class`, `y`, `status`, `churn`. Note the dtype (object/string/bool/category or ints) and the number of distinct classes if outputs show it.
- **How the target lives in the notebook.** Two common shapes:
  - separate objects: `y_train`, `y_test`, `y_val` (Series or arrays);
  - a column inside DataFrames: `train_df['target']`, `test_df['target']`, `val_df['target']`.
- **Which splits exist.** Train and test are expected; validation is optional. Use the variable names the notebook already uses.
- **Whether encoding was already done.** If a `LabelEncoder` already exists or the target is already numeric, tell the user instead of encoding twice.

If the splits are not made yet, tell the user the target should be encoded after the split so the encoder only ever sees training labels, and ask whether to proceed once the split cell exists.

### 2. Confirm the target with the user

Always confirm the target column, even when it looks obvious, because encoding the wrong column silently corrupts the data. Use `AskUserQuestion` with the candidates you found (best guess first, marked recommended), or ask in plain text if that tool isn't available. Include in the question the split variable names you plan to use, so one answer settles both. Do not add cells until they answer.

### 3. Add the cells

Add cells right after the cell where the splits are created (or at the end if that's unclear), using the notebook edit tool. Put a short markdown cell above the code cell explaining what it does. Keep the code cells small and readable so the user can follow them.

Use this pattern. Adapt names to the notebook, and drop the validation lines if there is no validation set.

**Cell A: fit and transform, saved in place**

```python
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

# Fit on the training target only, so nothing from test/validation leaks into the encoder
y_train = label_encoder.fit_transform(y_train)

# Reuse the training mapping for the other splits
y_test = label_encoder.transform(y_test)
y_val = label_encoder.transform(y_val)   # only if a validation target exists
```

If the target is a DataFrame column, keep the same shape of assignment:

```python
train_df['target'] = label_encoder.fit_transform(train_df['target'])
test_df['target'] = label_encoder.transform(test_df['target'])
val_df['target'] = label_encoder.transform(val_df['target'])   # only if present
```

The result goes back into the same variable or column, as the user asked, so no downstream cell needs renaming. Note that `fit_transform` on a pandas Series returns a NumPy array. That is fine for `y_train`-style variables. For DataFrame columns the assignment handles it.

**Cell B: show the mapping**, so the user can see what each number means and can trust the decode step later:

```python
mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
print(mapping)
```

Keep the encoder in the variable `label_encoder` (unless the notebook already uses another name). It must stay in memory, since `inverse_transform` needs it later.

### 4. Guard against the usual failure modes

- **Unseen labels in test/validation.** `transform` raises `ValueError` for a label that never appeared in training. Don't silently drop or remap rows. Tell the user which labels are unseen and let them decide (fix the split, stratify it, or merge classes).
- **Missing values in the target.** `LabelEncoder` doesn't handle NaN cleanly. If the target has nulls, flag it and ask how to handle them before encoding.
- **Re-running the cell.** Encoding an already-encoded variable would fail or corrupt values. It's worth mentioning that Cell A should be run once per fresh split, or guard it with a check such as `if not np.issubdtype(np.asarray(y_train).dtype, np.number):` when the notebook is likely to be re-run top to bottom.
- **Mixed types.** If labels mix strings and numbers, the encoder will error. Surface it and ask.

### 5. Run and verify if you can

If a kernel or `jupyter nbconvert --execute` is available, run the new cells and check the output: the mapping prints, the dtypes are numeric, and the class count matches expectations. If you can't execute, say so and tell the user which cells to run.

## Part 2: Decode with inverse_transform

Trigger this when the user wants labels back in their original form, for example "convert the predictions back," "show the original labels," or "decode y_pred."

1. Find the variable(s) to decode. This is usually predictions (`y_pred`, `y_pred_val`) and sometimes the encoded targets themselves (`y_test`). If it isn't clear from the notebook or the request, ask which variable(s).
2. Confirm `label_encoder` still exists in the notebook. If the encoder was never fitted (or the notebook was restarted and cells haven't been re-run), tell the user and offer to add the encoding cells first.
3. Ask the user whether to decode into the **same variable** or a **different (new) variable**, unless they already said. Use `AskUserQuestion` (or plain text if unavailable) and put both choices in one question covering all the variables being decoded. Overwriting is simpler, but the numeric version is gone afterwards, which matters if a later cell computes metrics or feeds a model. Offer a sensible new name for each variable (for example `y_pred_labels`, `y_test_labels`) so the "different variable" option is one click.
4. Add a markdown cell and a code cell using the answer:

```python
# Same variable: overwrite with the original labels
y_test = label_encoder.inverse_transform(y_test)
y_pred = label_encoder.inverse_transform(y_pred)

# Different variable: keep the numeric version and add a decoded copy
y_test_labels = label_encoder.inverse_transform(y_test)
y_pred_labels = label_encoder.inverse_transform(y_pred)
```

Only include the block that matches the user's choice. If they choose different variables, use the names you offered (or the ones they gave) and leave the originals untouched.

Warn once if the user chooses to overwrite a variable that a later cell still feeds to a model or a metric: those cells expect the numeric form, so decoding in place should come after training and evaluation.

## Reporting back

Keep the summary short: which column was encoded, which splits were transformed, the class mapping, where the new cells sit in the notebook, and anything you flagged (unseen labels, nulls, whether the cells were run).
