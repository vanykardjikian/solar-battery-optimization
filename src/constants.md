# `src/constants.py`

## Purpose

This module centralizes all numerical inputs for the optimization problem.

## Contents

### Time index

- **`T`**: `range(24)` for hourly steps (t = 0,...,23).

### Electricity purchase tariff (grid import)

- **`C_buy[t]`** (AMD/kWh): time-of-use tariff used when buying from the grid.
  - Off-peak: hours **0-6** and **23** -> 38 AMD/kWh
  - Peak: hours **7-22** -> 52 AMD/kWh

### Solar generation and demand profiles

- **`E_solar[t]`**: PV generation in hour t
- **`E_demand[t]`**: building load in hour t

### Battery parameters

- **`E_cap`** (kWh): energy capacity
- **`P_charge_max`**, **`P_discharge_max`** (kW): max charge/discharge per hour
- **`charge_eff`**, **`discharge_eff`**: battery efficiencies.
- **`s0`** (kWh): initial battery state of charge (SOC)

### Grid transaction limits

- **`P_buy_max`** (kW): max grid import per hour
- **`P_sell_max`** (kW): max grid export per hour

### Loss coefficient

- **`k`**: quadratic loss coefficient

## Used by

- `linear.py` and `non_linear.py` for optimization model parameters
- `main.py` for the workflow input overview plot
