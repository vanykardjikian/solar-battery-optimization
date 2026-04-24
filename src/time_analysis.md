# `src/time_analysis.py`

## Purpose

Provides a timing benchmark comparing MILP solve time (PuLP/CBC) and MINLP solve time (GEKKO/APOPT), under the same 24-hour scenario, without generating CSV or plots.

## Method

- Repeats each solver call `N_RUNS = 10` times
- Uses `time.perf_counter()` for timing
- Calls both solvers with `save_results=False` so only the optimization solve is measured

## How to run

From `src/`:

```bash
python time_analysis.py
```
