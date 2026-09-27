# Train/Test Split Summary

**Date:** 2026-09-27
**Source dataframe:** `df` — shape (1000, 7)
**Target column (y):** `species`
**Features (X):** all remaining 6 columns — `island`, `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`

## Split configuration
- Split type: Train / Test
- Test size: 0.2 (20%)
- random_state: 42
- Stratify: yes, on `species`

## Resulting shapes
| Split | X shape   | y shape |
|-------|-----------|---------|
| Train | (800, 6)  | (800,)  |
| Test  | (200, 6)  | (200,)  |

## Class balance (stratification check)
| Species   | Full dataset | Train | Test |
|-----------|-------------|-------|------|
| Adelie    | 46.1%       | 46.1% | 46.0% |
| Gentoo    | 28.8%       | 28.8% | 29.0% |
| Chinstrap | 25.1%       | 25.1% | 25.0% |

Class proportions are preserved almost exactly across train and test sets, as expected with `stratify=y`.
