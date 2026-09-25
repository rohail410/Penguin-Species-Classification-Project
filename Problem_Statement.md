# Problem Statement: Penguin Species Classification

## What this project is about

This project works with a dataset of 1,000 penguin observations (`data/Penguin Species Prediction Dataset.csv`), each described by seven fields:

- **species** — the target label, one of `Adelie` (461 records), `Chinstrap` (251), or `Gentoo` (288)
- **island** — the island where the penguin was observed: `Dream` (527), `Biscoe` (302), or `Torgersen` (171)
- **culmen_length_mm** and **culmen_depth_mm** — bill dimensions
- **flipper_length_mm** — flipper length
- **body_mass_g** — body mass
- **sex** — `Male` or `Female`

The dataset is a version of the well-known Palmer Archipelago penguins data, covering three species observed across three islands in Antarctica.

## The core problem

**Given a penguin's physical measurements (bill length/depth, flipper length, body mass) and where it was observed, can we accurately predict which of the three species it belongs to?**

This is framed as a supervised, multi-class classification problem: `species` is the target variable, and the remaining fields (`island`, `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`) are candidate predictors.

Notably, the data already hints that this is a learnable problem rather than a noisy one: species and island are strongly associated (Gentoo appears only on Biscoe, Chinstrap only on Dream, and Adelie appears on all three), and the numeric measurements show visibly different distributions across species — suggesting that even simple models should be able to separate the classes reasonably well.

## Why it matters

This is a learning/portfolio project. The goal is to practice and demonstrate an end-to-end classification workflow — exploratory data analysis, handling missing data, feature encoding, model selection, and evaluation — using a clean, well-understood dataset where the "right answer" behavior is well documented in the broader data science community. It's a vehicle for building and showing applied ML skills rather than solving an active real-world decision problem.

