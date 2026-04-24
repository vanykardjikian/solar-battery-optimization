# Optimal Allocation of Energy Resources of a Grid Connected Microsystem: Nonlinear Case

This project simulates a 24‑hour operation of a grid-connected microsystem that has
solar PV, battery storage, and the ability to buy from or sell to the grid. It
bundles both a **Mixed Integer Linear Program (MILP)** implemented in PuLP and a
**Mixed Integer Non-Linear Program (MINLP)** formulation built with GEKKO for comparison.

---

## Repository Layout

| Path | Purpose |
|------|---------|
| `src/main.py` | Runs both solvers, comparison plot, and sensitivity charts |
| `src/time_analysis.py` | Solver timing benchmarks |
| `src/constants.py` | System parameters |
| `src/profiles.py` | Helper for building hourly sell-price profiles |
| `src/linear.py` | Linear PuLP/CBC MILP implementation |
| `src/non_linear.py` | Nonlinear GEKKO implementation |
| `src/charts.py` | All Matplotlib plotting helpers |
| `results/` | Auto-generated CSV tables and PNG figures |

---

## Getting Started

### 1. Install dependencies

```bash
pip install pulp pandas matplotlib gekko
```

### 2. Run the simulations

```bash
python -m src.main
```

The script creates `results/linear/` and `results/non_linear/` if they do not
exist, runs both scenarios for each solver, generates comparison plots, and
executes a sensitivity sweep.

### 3. Inspect outputs

- Scenario CSV tables and figures: `results/<solver>/<scenario>_*.{csv,png}`
- Combined comparison chart: `results/comparison.png`
- Solar vs demand overview: `results/solar_vs_demand.png`
- Sensitivity charts: `results/<solver>/<solver>_sensitivity_analysis.png`

### 4. Comparing solver times

To benchmark the linear (PuLP/CBC) and non-linear (GEKKO) solvers without generating any outputs.

```bash
cd src
python time_analysis.py
```

The script runs the same 24-hour scenario 10 times per solver (solver-only, no CSV or charts), then prints the average solve time and the ratio. Use these numbers to compare computational performance.

---

## Extending the Project

- Modify `constants.py` to change the physical system or costs.
- Build new tariff shapes via `profiles.variable_tariff_profile`.

---

## License

MIT License.