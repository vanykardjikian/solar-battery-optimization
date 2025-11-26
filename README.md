# Microgrid Optimization

This project simulates a 24‑hour operation of a grid-connected prosumer that has
solar PV, battery storage, and the ability to buy from or sell to the grid. It
bundles both a **Mixed Integer Linear Program (MILP)** implemented in PuLP and a
**Mixed Integer Non-Linear Program (MILP)** formulation built with GEKKO so you can compare dispatch
strategies and economics.

---

## Highlights

- Centralized system parameters in `constants.py`
- Reusable tariff builders in `profiles.py` (e.g., 7h off-peak + 16h peak)
- Linear MILP (`linear.py`) solved with PuLP + CBC
- Non-linear MINLP (`non_linear.py`) solved with GEKKO
- Automated scenario runner in `main.py`:
  - Scenario 1: flat export price of 22 AMD/kWh
  - Scenario 2: off-peak 35 AMD/kWh, peak 48 AMD/kWh
- Sensitivity analysis that explores sell prices and plots exports vs. cost
- Rich Matplotlib charts saved under `results/linear/` and `results/non_linear/`

---

## Model Summary

Both solvers enforce the same physics and constraints over 24 hourly periods:

- Power balance each hour: solar + grid buy + discharge = demand + charge + export
- Battery state-of-charge recursion with charge/discharge efficiencies
- Bounds on grid transactions and battery power
- Binary charge/discharge indicators to prevent simultaneous actions
- Grid buy/sell exclusivity (handled via bounds or binaries per solver)

### Decision Variables (linear model notation)

| Variable | Description |
|----------|-------------|
| `xtbuy[t]` | Energy purchased from the grid |
| `xtsell[t]` | Energy exported to the grid |
| `xtcharge[t]` | Battery charging power |
| `xtdischarge[t]` | Battery discharging power |
| `st[t]` | Battery state of charge |
| `ytcharge[t]`, `ytdischarge[t]` | Binary charge/discharge toggles |

The GEKKO model mirrors these variables and binaries to keep results comparable.

---

## Repository Layout

| Path | Purpose |
|------|---------|
| `main.py` | Runs both solvers, comparison plot, and sensitivity charts |
| `constants.py` | Battery, solar, demand, and grid price parameters |
| `profiles.py` | Helpers for building hourly sell-price profiles |
| `linear.py` | PuLP/CBC MILP implementation |
| `non_linear.py` | GEKKO implementation |
| `charts.py` | All Matplotlib plotting helpers |
| `results/` | Auto-generated CSV tables and PNG figures |

---

## Getting Started

### 1. Install dependencies

```bash
pip install pulp pandas matplotlib gekko
```

### 2. Run the simulations

```bash
python main.py
```

The script creates `results/linear/` and `results/non_linear/` if they do not
exist, runs both scenarios for each solver, generates comparison plots, and
executes a sensitivity sweep.

### 3. Inspect outputs

- Scenario CSV tables and figures: `results/<solver>/<scenario>_*.{csv,png}`
- Combined comparison chart: `results/comparison.png`
- Solar vs demand overview: `results/solar_vs_demand.png`
- Sensitivity charts: `results/<solver>/<solver>_sensitivity_analysis.png`

---

## Extending the Project

- Modify `constants.py` to change the physical system or costs.
- Build new tariff shapes via `profiles.variable_tariff_profile`.

---

## License

MIT License.