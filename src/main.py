import os
import linear
import non_linear
from constants import T, Esolar, Edemand
from profiles import variable_tariff_profile
import charts

os.makedirs("results", exist_ok=True)
os.makedirs("results/linear", exist_ok=True)
os.makedirs("results/non_linear", exist_ok=True)

charts.solar_vs_demand(T, Esolar, Edemand)

scenario1_prices = variable_tariff_profile(22, 22)
scenario2_prices = variable_tariff_profile(35, 48)

# --- Linear solver ---
print("Running linear scenarios...")
df1l = linear.solve_scenario(scenario1_prices, "(Linear) Scenario 1 - 22 AMD", "results/linear")
df2l = linear.solve_scenario(scenario2_prices, "(Linear) Scenario 2 - 35 or 48 AMD", "results/linear")

# --- Non-linear solver ---
print("Running non-linear scenarios...")
df1nl = non_linear.solve_scenario(scenario1_prices, "(Non-linear) Scenario 1 - 22 AMD", "results/non_linear")
df2nl = non_linear.solve_scenario(scenario2_prices, "(Non-linear) Scenario 2 - 35 or 48 AMD", "results/non_linear")
charts.comparison_chart(df1l, df2l, df1nl, df2nl)

# --- Sensitivity plot ---
print("\nRunning sensitivity analysis...")

charts.sensitivity_chart(linear.solve_scenario, '(Linear)', "results/linear")
charts.sensitivity_chart(non_linear.solve_scenario, '(Non-linear)', "results/non_linear")


print("\n" + "=" * 60)
print("ALL DONE! Check the 'results/' folder:")
