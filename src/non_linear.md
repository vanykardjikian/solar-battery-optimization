# `src/non_linear.py`

## Purpose

Implements the Mixed-Integer Nonlinear Programming model of the same 24-hour scheduling problem as `linear.py`, but with quadratic loss terms to better represent inverter/battery losses.

- Modeling/solver framework: **GEKKO**
- MINLP solver: **APOPT** (selected by `m.options.SOLVER = 1`, solved locally)


## Main function

### `solve_scenario(C_sell, scenario_name, results_folder, save_results=True)`

Inputs/outputs match the linear version:

- `save_results=True`: return `DataFrame`, save CSV and figures
- `save_results=False`: return summary dict (used for sensitivity and timing)

## Mathematical model

Variables, objective and bounds are the same as the linear model.

### Nonlinear constraint

The SOC constraint includes an additional loss term per hour:

`s[t] = s[t-1] + charge_eff*x_charge[t] - x_discharge[t] / discharge_eff - loss[t]`

Where:

`loss[t] = k * (x_charge[t]**2 / P_charge_max + x_discharge[t]**2 / P_discharge_max)`

The rest of the constraints match the linear model.

## Artifacts

Produces the same CSV file and plots as `linear.py`.
