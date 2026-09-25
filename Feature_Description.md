# Feature Description: Penguin Species Prediction Dataset

Source file: `data/Penguin Species Prediction Dataset.csv`

Dataset shape: 1000 rows x 7 columns

## Summary Table

| Column | Type | % Missing | Notes |
|---|---|---|---|
| species | Categorical (target) | 0% | 3 classes |
| island | Categorical | 0% | 3 islands |
| culmen_length_mm | Float | 1.0% | Bill length in mm |
| culmen_depth_mm | Float | 1.0% | Bill depth in mm |
| flipper_length_mm | Float | 1.0% | Flipper length in mm |
| body_mass_g | Float | 1.0% | Body mass in grams |
| sex | Categorical | 1.0% | Male/Female |

---

## species
- **Description:** The penguin species, the target variable for classification.
- **Type:** Categorical (nominal), 3 classes.
- **Examples:** Adelie, Gentoo, Chinstrap
- **Data Quality Issues:** None observed. No missing values. Class distribution is moderately imbalanced: Adelie 461 (46.1%), Gentoo 288 (28.8%), Chinstrap 251 (25.1%).

## island
- **Description:** The island in the Palmer Archipelago (Antarctica) where the penguin was observed.
- **Type:** Categorical (nominal), 3 classes.
- **Examples:** Torgersen, Biscoe, Dream
- **Data Quality Issues:** None observed. No missing values, no inconsistent spelling/casing. Distribution: Dream 527, Biscoe 302, Torgersen 171.

## culmen_length_mm
- **Description:** Length of the penguin's culmen (bill), in millimeters.
- **Type:** Float (continuous numeric).
- **Examples:** 48.6, 39.7, 47.8, 46.9, 32.4
- **Data Quality Issues:** 10 missing values (1.0%). Range (32.4–56.0mm) and distribution look biologically plausible with no negative values or extreme outliers.

## culmen_depth_mm
- **Description:** Depth of the penguin's culmen (bill), in millimeters.
- **Type:** Float (continuous numeric).
- **Examples:** 15.5, 15.0, 16.2, 19.4, 13.0
- **Data Quality Issues:** 10 missing values (1.0%). Range (13.0–21.4mm) looks plausible, no negative values or extreme outliers.

## flipper_length_mm
- **Description:** Length of the penguin's flipper, in millimeters.
- **Type:** Float (continuous numeric), though the underlying quantity is effectively integer-valued measurements stored as floats.
- **Examples:** 218.0, 185.0, 221.0, 193.0, 175.0
- **Data Quality Issues:** 10 missing values (1.0%). Range (175–235mm) looks plausible, no negative values or extreme outliers.

## body_mass_g
- **Description:** Body mass of the penguin, in grams.
- **Type:** Float (continuous numeric).
- **Examples:** 3923.0, 4195.0, 3519.0, 5858.0, 2830.0
- **Data Quality Issues:** 10 missing values (1.0%). Range (2830–6317g) looks plausible for the three species, no negative values or implausible extremes.

## sex
- **Description:** The sex of the penguin.
- **Type:** Categorical (binary).
- **Examples:** Male, Female
- **Data Quality Issues:** 10 missing values (1.0%). Only two clean categories present (Male: 528, Female: 462), no inconsistent casing or stray values (e.g. no "."  or "unknown" placeholders as sometimes seen in similar penguin datasets).

---

## Cross-Column Observations
- **Missingness pattern:** 951 rows have no missing values, 48 rows have exactly one missing value, and 1 row has two missing values. Missingness is scattered independently across columns/rows rather than concentrated in a block of fully-empty records, and does not appear concentrated in any single species or island.
- **Duplicates:** No fully duplicate rows found.
- **No ID column:** The dataset has no unique identifier column for individual penguins.
