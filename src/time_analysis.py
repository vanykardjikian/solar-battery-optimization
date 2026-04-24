"""
Measures the average solve time of the linear and nonlinear optimization models.

"""

import time

import linear
import non_linear
from profiles import variable_tariff_profile

N_RUNS = 10


def main():
    prices = variable_tariff_profile(22, 22)
    print(f"Solver timing ({N_RUNS} runs each)...")

    times_linear = []
    for _ in range(N_RUNS):
        t0 = time.perf_counter()
        linear.solve_scenario(prices, "", "", save_results=False)
        times_linear.append(time.perf_counter() - t0)

    times_nonlinear = []
    for _ in range(N_RUNS):
        t0 = time.perf_counter()
        non_linear.solve_scenario(prices, "", "", save_results=False)
        times_nonlinear.append(time.perf_counter() - t0)

    t_linear = sum(times_linear) / N_RUNS
    t_nonlinear = sum(times_nonlinear) / N_RUNS

    print("\n" + "=" * 50)
    print(f"Linear (PuLP/CBC)\t{t_linear:.3f} s\t(avg of {N_RUNS})")
    print(f"Non-linear (GEKKO)\t{t_nonlinear:.3f} s\t(avg of {N_RUNS})")
    if t_linear > 0:
        print(f"Ratio (non-linear/linear)\t{t_nonlinear/t_linear:.1f}x")
    print("=" * 50)


if __name__ == "__main__":
    main()
