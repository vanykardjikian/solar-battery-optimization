# `src/linear.py`

## Purpose

Implements the Mixed-Integer Linear Programming model for optimal 24-hour energy scheduling of the grid-connected system.

- Modeling framework: **PuLP**
- Solver: **CBC** (COIN-OR, branch-and-cut)

The linear model assumes constant efficiency and serves as the benchmark for comparing against the nonlinear loss-aware formulation.

## Main function

### `solve_scenario(C_sell, scenario_name, results_folder, save_results=True)`

Solves one tariff scenario.

#### Inputs

- **`C_sell`**: 24-hour export price profile (AMD/kWh)
- **`scenario_name`**: label used in filenames
- **`results_folder`**: where CSV/plots are saved
- **`save_results`**:
  - `True`: save CSV and generate plots
  - `False`: return summary only (used for sensitivity analysis / timing)

#### Outputs

- If `save_results=True`: returns a `pandas.DataFrame` and writes a CSV table with 24 rows (hours).
- If `save_results=False`: returns a `dict` with `exported`, `actual_cost`, and `baseline_cost`.

## Mathematical model

### Decision variables (per hour t)

- `x_buy[t]` : grid import
- `x_sell[t]` : grid export
- `x_charge[t]` : battery charge
- `x_discharge[t]` : battery discharge
- `s[t]` : state of charge
- `y_charge[t]`, `y_discharge[t]` : binary charge/discharge decision variables 

### Objective

Maximize net revenue (equivalently minimize net cost):

`for (t = 0,.. ,23`:

- Maximize: `sum_t (C_sell[t] * xsell[t] - C_buy[t] * xbuy[t])`

### Constraints (per hour `t`)

- **Energy balance**
  - `E_solar[t] + x_buy[t] + x_discharge[t] = E_demand[t] + xcharge[t] + xsell[t]`

- **SOC (linear efficiency)**
  - `s[t] = s[t-1] + charge_eff * xcharge[t] - xdischarge[t] / discharge_eff`

- **No simultaneous charge and discharge**
  - `ycharge[t] + ydischarge[t] <= 1`

- **Power limits**
  - `xcharge[t] <= P_charge_max * ycharge[t]`
  - `xdischarge[t] <= P_discharge_max * ydischarge[t]`

- **Grid limits**
  - `xbuy[t] <= P_buy_max`
  - `xsell[t] <= P_sell_max`

## Artifacts (when `save_results=True`)

The function saves:

- a CSV table of the solution
- 5 figures via `charts.py` (scenario chart, cost structure, sources, decision variables, battery behavior).
