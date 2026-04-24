import os
import linear
import non_linear
from constants import T, E_solar, E_demand
from profiles import variable_tariff_profile
import charts

results_folder = "results"
linear_folder = f"{results_folder}/linear"
non_linear_folder = f"{results_folder}/non_linear"

os.makedirs(results_folder, exist_ok=True)
os.makedirs(linear_folder, exist_ok=True)
os.makedirs(non_linear_folder, exist_ok=True)

charts.solar_vs_demand_chart(T, E_solar, E_demand, results_folder)

scenario1_prices = variable_tariff_profile(22, 22)
scenario2_prices = variable_tariff_profile(35, 48)

# --- Linear solver ---
print("Running linear scenarios...")
df1l = linear.solve_scenario(scenario1_prices, "(Linear) Scenario 1 - 22 AMD", linear_folder)
df2l = linear.solve_scenario(scenario2_prices, "(Linear) Scenario 2 - 35 or 48 AMD", linear_folder)

# --- Non-linear solver ---
print("Running non-linear scenarios...")
df1nl = non_linear.solve_scenario(scenario1_prices, "(Non-linear) Scenario 1 - 22 AMD", non_linear_folder)
df2nl = non_linear.solve_scenario(scenario2_prices, "(Non-linear) Scenario 2 - 35 or 48 AMD", non_linear_folder)
charts.comparison_chart(df1l, df2l, df1nl, df2nl, results_folder)

# --- Sensitivity plot ---
print("\nRunning sensitivity analysis...")
charts.sensitivity_chart(linear.solve_scenario, "(Linear)", linear_folder)
charts.sensitivity_chart(non_linear.solve_scenario, "(Non-linear)", non_linear_folder)

print("\n" + "=" * 60)
print(f"\nALL DONE! Check the '{results_folder}/' folder:")
