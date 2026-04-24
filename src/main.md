# `src/main.py`

## Purpose

Runs the complete workflow:

- creates output directories
- plots input profiles
- solves two tariff scenarios with the linear and nonlinear models
- generates comparison and sensitivity figures

## Workflow summary

1. Create `results/`, `results/linear/`, `results/non_linear/`
2. Plot solar vs demand chart
3. Construct two export-price scenarios via `profiles.variable_tariff_profile`
4. Run `linear.solve_scenario` for both scenarios (CSV + plots)
5. Run `non_linear.solve_scenario` for both scenarios (CSV + plots)
6. Create the combined comparison chart
7. Run sensitivity analysis for both solvers

## How to run

From the repository root:

```bash
python -m src.main
```
