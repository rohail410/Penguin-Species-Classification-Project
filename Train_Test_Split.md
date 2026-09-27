# Train/Test Split Summary

**Date:** 2026-09-27
**Source dataframe:** `df` — shape (1000, 7)
**Target column (y):** `species`
**Features (X):** all other columns (6 columns): `island`, `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`

## Split configuration
- Split type: Train / Test
- Test size: 0.2 (20%)
- random_state: 42
- Stratify: yes, on `species`

## Resulting shapes

| Split | X shape    | y shape |
|-------|------------|---------|
| Train | (800, 6)   | (800,)  |
| Test  | (200, 6)   | (200,)  |

## Class balance (stratification check)

| Species   | Train count | Train % | Test count | Test % | Overall % |
|-----------|-------------|---------|------------|--------|-----------|
| Adelie    | 369         | 46.1%   | 92         | 46.0%  | 46.1%     |
| Gentoo    | 230         | 28.75%  | 58         | 29.0%  | 28.8%     |
| Chinstrap | 201         | 25.1%   | 50         | 25.0%  | 25.1%     |

Stratification kept each species' proportion within a few tenths of a percent between train and test, matching the overall dataset distribution.
