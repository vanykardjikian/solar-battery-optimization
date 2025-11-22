from pulp import LpProblem, LpVariable, LpMaximize, LpBinary, value, PULP_CBC_CMD
import pandas as pd
import os

import charts

# Create results folder
os.makedirs("results", exist_ok=True)

# Parameters
T = range(24)

C_buy  = [38]*7 + [52]*17
Esolar = [0]*7 + [1, 4, 10, 18, 28, 36, 40, 41, 38, 32, 22, 12, 5, 2] + [0]*3
Edemand = [5, 5, 5, 5, 5, 5, 10, 10, 25, 25, 25, 25, 20, 20, 30, 30, 30, 30, 15, 15, 8, 8, 8, 8 ]

Ecap             = 30
Pcharge_max      = 12
Pdischarge_max   = 12
charge_eff       = 0.95
discharge_eff    = 0.95
s0               = 15
Pbuy_max         = 60
Psell_max        = 30

charts.solar_vs_demand(T, Esolar, Edemand)

# === Solver function ===
def solve_scenario(export_price, scenario_name, save_results = True):
    C_sell = [export_price] * 24
    baseline_cost = sum(C_buy[t] * Edemand[t] for t in T)

    model = LpProblem(f"Microgrid_{scenario_name}", LpMaximize)

    # Variables
    xbuy       = LpVariable.dicts("xtbuy",       T, 0, Pbuy_max)
    xsell      = LpVariable.dicts("xtsell",      T, 0, Psell_max)
    xcharge    = LpVariable.dicts("xtcharge",    T, 0, Pcharge_max)
    xdischarge = LpVariable.dicts("xtdischarge", T, 0, Pdischarge_max)
    s          = LpVariable.dicts("st",          T, 0, Ecap)
    ycharge    = LpVariable.dicts("ytcharge",    T, cat=LpBinary)
    ydischarge = LpVariable.dicts("ytdischarge", T, cat=LpBinary)
    ybuy       = LpVariable.dicts("ytbuy",       T, cat=LpBinary)
    ysell      = LpVariable.dicts("ytsell",      T, cat=LpBinary)

    # Objective
    model += sum(C_sell[t]*xsell[t] - C_buy[t]*xbuy[t] for t in T)

    # Constraints
    for t in T:
        model += Esolar[t] + xbuy[t] + xdischarge[t] == Edemand[t] + xcharge[t] + xsell[t]

        if t == 0:
            model += s[t] == s0 + charge_eff * xcharge[t] - xdischarge[t] / discharge_eff
        else:
            model += s[t] == s[t-1] + charge_eff * xcharge[t] - xdischarge[t] / discharge_eff

        model += xcharge[t]    <= Pcharge_max    * ycharge[t]
        model += xdischarge[t] <= Pdischarge_max * ydischarge[t]
        model += ycharge[t] + ydischarge[t] <= 1

        model += xbuy[t]    <= Pbuy_max    * ybuy[t]
        model += xsell[t] <= Psell_max * ysell[t]
        model += ybuy[t] + ysell[t] <= 1


    model.solve(PULP_CBC_CMD(msg=False))

    # === Extract results ===
    data = []
    for t in T:
        data.append({
            "Hour": t,
            "Solar": Esolar[t],
            "Demand": Edemand[t],
            "Buy": value(xbuy[t]),
            "Sell": value(xsell[t]),
            "Charge": value(xcharge[t]),
            "Discharge": value(xdischarge[t]),
            "SOC": value(s[t]),
            "y_c": int(value(ycharge[t])),
            "y_d": int(value(ydischarge[t])),
            "y_s": int(value(ysell[t])),
            "y_b": int(value(ybuy[t])),
        })
    df = pd.DataFrame(data)

    actual_cost = value(model.objective)
    exported = df["Sell"].sum()

    if not save_results:
        return {
            'exported': exported,
            'actual_cost': actual_cost,
            'baseline_cost': baseline_cost
        }

    df.to_csv(f"results/{scenario_name.replace(' ', '_')}_table.csv", index=False)

    print(f"\n{'='*60}")
    print(f"{scenario_name} | Export price: {export_price} AMD/kWh")
    print(f"{'='*60}")
    print(df.round(2).to_string(index=False))
    print(f"→ Baseline Cost: {baseline_cost:.0f} AMD | Actual Cost: {actual_cost:.0f} AMD | Exported: {exported:.1f} kWh")

    # === Plots ===
    charts.scenario_chart(df, actual_cost, exported, scenario_name)
    charts.costs_chart(df, C_buy, export_price, actual_cost, T, scenario_name)
    charts.sources_chart(df, scenario_name)
    charts.decision_variables(df, scenario_name)
    charts.battery_charging(df, scenario_name)

    return {
        'df': df,
        'exported': exported,
        'actual_cost': actual_cost,
        'baseline_cost': baseline_cost
    }

# Run both scenarios
print("Running scenarios with your exact data...")
results1 = solve_scenario(22, "Scenario 1 - 22 AMD")
results2 = solve_scenario(48, "Scenario 2 - 48 AMD")
charts.plot_comparison(results1['df'], results2['df'])


# Sensitivity plot
print("\nRunning sensitivity analysis...")

charts.sensitivity_chart(solve_scenario)

print("\n" + "="*60)
print("ALL DONE! Check the 'results/' folder:")
