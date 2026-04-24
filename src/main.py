import os

import charts
import linear
import non_linear
from constants import E_demand, E_solar, T
from profiles import variable_tariff_profile

RESULTS_FOLDER = "results"
LINEAR_FOLDER = f"{RESULTS_FOLDER}/linear"
NON_LINEAR_FOLDER = f"{RESULTS_FOLDER}/non_linear"

os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(LINEAR_FOLDER, exist_ok=True)
os.makedirs(NON_LINEAR_FOLDER, exist_ok=True)

charts.solar_vs_demand_chart(T, E_solar, E_demand, RESULTS_FOLDER)

scenario1_prices = variable_tariff_profile(22, 22)
scenario2_prices = variable_tariff_profile(35, 48)

# --- Linear solver ---
print("Running linear scenarios...")
df1l = linear.solve_scenario(
    scenario1_prices, "(Linear) Scenario 1 - 22 AMD", LINEAR_FOLDER
)
df2l = linear.solve_scenario(
    scenario2_prices, "(Linear) Scenario 2 - 35 or 48 AMD", LINEAR_FOLDER
)

# --- Non-linear solver ---
print("Running non-linear scenarios...")
df1nl = non_linear.solve_scenario(
    scenario1_prices, "(Non-linear) Scenario 1 - 22 AMD", NON_LINEAR_FOLDER
)
df2nl = non_linear.solve_scenario(
    scenario2_prices, "(Non-linear) Scenario 2 - 35 or 48 AMD", NON_LINEAR_FOLDER
)
charts.comparison_chart(df1l, df2l, df1nl, df2nl, RESULTS_FOLDER)

# --- Sensitivity plot ---
print("\nRunning sensitivity analysis...")
charts.sensitivity_chart(linear.solve_scenario, "(Linear)", LINEAR_FOLDER)
charts.sensitivity_chart(non_linear.solve_scenario, "(Non-linear)", NON_LINEAR_FOLDER)

print("\n" + "=" * 60)
print(f"\nALL DONE! Check the '{RESULTS_FOLDER}/' folder:")
