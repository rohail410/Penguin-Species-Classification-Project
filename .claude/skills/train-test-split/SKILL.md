---
name: train-test-split
description: Use this skill whenever the user asks to split data into train/test sets, train/validation/test sets, or asks for X_train, X_test, y_train, y_test, X_val, or y_val inside a Jupyter notebook (.ipynb). Also trigger on requests like "split my dataframe for modeling", "prepare train and test sets", "add a train test split to my notebook", or "I need a validation set too" when a dataframe already exists in the notebook. This skill adds working code cells to the notebook itself (not just chat code), confirms every choice (dataframe, target column, split type, ratios, random_state, stratify) with the user before writing anything, runs the notebook to get real shapes, and produces a markdown summary document with the actual resulting numbers. Make sure to use this skill even if the user only says "split the data" or "hold out a validation set" without spelling out train_test_split by name, as long as the context is a notebook with a dataframe.
---

# Train/Test/Validation Split for Notebooks

## Why this skill exists

Splitting data sounds like a one-line `sklearn` call, but in practice it's a series of small decisions (which column is the target, whether a validation set is needed, what ratios, whether to fix randomness, whether to stratify) that are cheap to get wrong and annoying to unwind once downstream cells depend on `X_train`/`y_train` names. This skill's job is to make each of those decisions explicit with the user, then write clean, verifiable cells directly into their notebook — not just paste code into chat — so the notebook is immediately usable for the next step of their workflow.

Because a wrong guess here (wrong target column, wrong dataframe, an unwanted stratify) means the user has to notice it, complain, and get cells rewritten, the guiding rule throughout is: **ask before you act, whenever there's any real ambiguity.** Don't ask about things that are genuinely unambiguous — but do ask rather than silently guess.

## Step 0 — Find the dataframe

Read the notebook (`Read` tool) and look for a pandas DataFrame the split should apply to — usually a variable assigned from `pd.read_csv`, `pd.read_excel`, a merge/groupby result, or similar, that is still "live" (not overwritten or dropped later) by the end of the notebook.

- If there's exactly one obvious candidate, tell the user which dataframe and variable name you found and ask them to confirm before proceeding ("Found `df` from the CSV load in cell 3 — is that the dataframe you want to split?").
- If there are multiple dataframes, or the notebook doesn't make it obvious which one is the "final" modeling dataframe, list the candidates you found and ask the user which one to use. Don't guess.
- If you can't find any dataframe at all, say so and ask the user for the variable name (they may not have run the loading cell yet, or it may live in an earlier notebook/file).

## Step 1 — Confirm the target (y) and features (X)

Ask the user which column(s) should be the target (`y`). Do not assume the last column, a column named `target`, or anything else — targets are domain-specific and guessing wrong here is the single most disruptive mistake this skill can make.

Once they answer, confirm your understanding back to them in plain terms before writing code, e.g.: "Got it — `y` will be the `churn` column, and `X` will be every other column in `df`. Sound right?" If the user wants to drop additional columns from `X` (IDs, leakage-prone columns, etc.), ask about that too rather than assuming `X` is just "everything else."

## Step 2 — Ask what kind of split is needed

Ask the user directly: do they want a **train/test split**, or a **train/validation/test split**? Don't infer this from earlier phrasing alone — confirm it as its own question, since it changes the whole cell structure.

### If train/test split:
Ask what ratio they want (e.g., "0.2" means 20% test, 80% train). If they say a number without units, treat it as the test fraction — but if it's at all ambiguous (e.g., they say "80/20" or "20%"), restate your interpretation and confirm: "Just to confirm — 80% train, 20% test?"

### If train/validation/test split:
Explain (briefly, if the user seems unsure) that this happens in two stages: first split off the test set, then split what's left into train and validation. Ask for:
1. The train+val vs. test ratio first.
2. Then, of the remaining train+val portion, how much should go to validation.

Confirm the resulting overall percentages back to the user before writing any cells, since "20% of the remaining 80%" is easy to get twisted. For example, if the user says 20% test, then 25% validation (of the remaining 80%), restate it as: "That works out to roughly 60% train / 20% validation / 20% test overall — is that what you want?"

If at any point the user seems unsure or confused about ratios, stop and explain rather than picking a default for them.

## Step 3 — Ask about random_state and stratify

Always ask both of these explicitly — never assume a default silently, even a common one like `random_state=42`:

- **random_state**: ask if they want the split to be reproducible (a fixed seed) and if so, which number to use (offer 42 as a common convention if they have no preference, but let them choose).
- **stratify**: ask if they want the split stratified on the target column (this matters most for classification tasks with imbalanced classes; for regression targets it usually doesn't apply). Briefly explain what it does if they seem unfamiliar with the term: it keeps the same proportion of each class in every split. If they want stratification, confirm it should stratify on `y` (or ask which column, if not obvious).

## Step 4 — Recap and get a final go-ahead

Before touching the notebook, give the user a short recap of every decision made so far (dataframe, target/features, split type, ratios, random_state, stratify) and ask them to confirm before you start editing. This is the last checkpoint before code gets written — it's much cheaper to fix a misunderstanding here than after cells are added and run.

## Step 5 — Add the cells to the notebook

Use the `NotebookEdit` tool (after `Read`-ing the notebook, which is required before any edit) to append new cells at the end of the notebook, in this order. Keep each step in its own cell rather than one large cell — the user should be able to see and re-run each stage independently, and the shape/head cells only make sense as separate, inspectable steps.

1. **Markdown cell** — a short header, e.g. `## Train/Test Split` or `## Train/Validation/Test Split`, so the added section is clearly demarcated from the user's existing work.
2. **Verification cell** — print the shape and `.head()` of the source dataframe, so the user can confirm the starting point before anything is split:
   ```python
   print("df shape:", df.shape)
   df.head()
   ```
3. **X/y split cell**:
   ```python
   X = df.drop(columns=["<target_column>"])
   y = df["<target_column>"]
   ```
4. **Split cell(s)**, using `sklearn.model_selection.train_test_split`, importing it if it's not already imported earlier in the notebook (check first — don't add a duplicate import).
   - Train/test only:
     ```python
     from sklearn.model_selection import train_test_split

     X_train, X_test, y_train, y_test = train_test_split(
         X, y, test_size=<test_fraction>, random_state=<seed_or_None>, stratify=<y_or_None>
     )
     ```
   - Train/validation/test (two sequential calls — split off test first, then split the remainder into train/val):
     ```python
     from sklearn.model_selection import train_test_split

     X_temp, X_test, y_temp, y_test = train_test_split(
         X, y, test_size=<test_fraction>, random_state=<seed_or_None>, stratify=<y_or_None>
     )
     X_train, X_val, y_train, y_val = train_test_split(
         X_temp, y_temp, test_size=<val_fraction_of_temp>, random_state=<seed_or_None>, stratify=<y_temp_or_None>
     )
     ```
   Omit `random_state=` and `stratify=` entirely (rather than passing `None` explicitly) if the user opted out of them — don't leave dead arguments in the code.
5. **Verification cell(s)** — print shape and `.head()` for every resulting split, so the user can immediately see the split worked as expected:
   ```python
   print("X_train shape:", X_train.shape)
   X_train.head()
   ```
   ```python
   print("X_test shape:", X_test.shape)
   X_test.head()
   ```
   (and the same for `X_val`/`y_val` if applicable; shapes for `y_*` are usually enough without `.head()` since they're single columns, but include whichever the user would find useful).

## Step 6 — Run the notebook to get real numbers

The markdown summary (next step) must contain the *actual* resulting shapes and percentages, not the requested ones restated — a requested 80/20 split can come out slightly different depending on rounding, and reporting real numbers is what makes the doc trustworthy as a record of what actually happened.

Execute the notebook to populate outputs. If there's no interactive kernel/execution tool available in this environment, run it non-interactively, e.g.:
```bash
jupyter nbconvert --to notebook --execute --inplace "<path/to/notebook.ipynb>"
```
Then `Read` the notebook again to pull the printed shapes out of the executed cell outputs. If execution fails (missing dependency, error in a cell unrelated to this skill's work, etc.), show the user the error rather than guessing at numbers, and ask how they'd like to proceed.

## Step 7 — Write the markdown summary document

Create a markdown file in the project folder (same directory as the notebook, unless the user says otherwise):
- `Train_Test_Split.md` for a train/test split
- `Train_Test_Validation_Split.md` for a train/validation/test split

Fill it in with the **real, post-run values** — don't template it with placeholders. Include:
- Source dataframe name and its shape
- Target column(s) used for `y`, and how `X` was derived
- Split type and the exact ratios used (both as requested and as they worked out numerically, if they differ)
- `random_state` used, or a note that none was set (results won't be reproducible run-to-run)
- Whether stratification was used, and on which column
- Resulting shapes of every split output (`X_train`, `y_train`, `X_test`, `y_test`, and `X_val`/`y_val` if applicable)
- The date the split was created

A simple structure works well:

```markdown
# Train/Test Split Summary

**Date:** <date>
**Source dataframe:** `df` — shape (<rows>, <cols>)
**Target column(s):** `<target>`
**Features (X):** all columns except `<target>` (<n_features> columns)

## Split configuration
- Split type: Train / Test
- Test size: 0.2 (20%)
- random_state: 42
- Stratify: yes, on `<target>`

## Resulting shapes
| Split   | X shape      | y shape   |
|---------|--------------|-----------|
| Train   | (<r>, <c>)   | (<r>,)    |
| Test    | (<r>, <c>)   | (<r>,)    |
```

For a train/validation/test split, add a `Validation` row to the table and note both the test fraction and the validation fraction (of the remaining train+val data), plus the overall effective percentages.

## Step 8 — Wrap up

Tell the user, in a couple of sentences, what was added (cells + the markdown file) and point them to the new cells and the doc. Don't re-paste the code or the full markdown content in chat — they can see it in the notebook and the file.
