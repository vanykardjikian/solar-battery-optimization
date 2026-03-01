from pulp import LpProblem, LpVariable, LpMaximize, LpBinary, value, PULP_CBC_CMD
import os
import pandas as pd

import charts
from constants import (
    T, C_buy, Esolar, Edemand, Ecap,
    Pcharge_max, Pdischarge_max, charge_eff, discharge_eff, s0,
    Pbuy_max, Psell_max,
)

os.makedirs("results", exist_ok=True)
charts.solar_vs_demand_chart(T, Esolar, Edemand)


def solve_scenario(C_sell, scenario_name, results_folder, save_results=True):
    baseline_cost = sum(C_buy[t] * Edemand[t] for t in T)

    model = LpProblem(f"Microgrid_{scenario_name}", LpMaximize)

    # --- Decision variables ---
    xbuy = LpVariable.dicts("xtbuy", T, 0, Pbuy_max)
    xsell = LpVariable.dicts("xtsell", T, 0, Psell_max)
    xcharge = LpVariable.dicts("xtcharge", T, 0, Pcharge_max)
    xdischarge = LpVariable.dicts("xtdischarge", T, 0, Pdischarge_max)
    s = LpVariable.dicts("st", T, 0, Ecap)
    ycharge = LpVariable.dicts("ytcharge", T, cat=LpBinary)
    ydischarge = LpVariable.dicts("ytdischarge", T, cat=LpBinary)

    # --- Objective: maximize revenue from export minus grid purchase cost ---
    model += sum(C_sell[t] * xsell[t] - C_buy[t] * xbuy[t] for t in T)

    # --- Constraints ---
    for t in T:
        model += Esolar[t] + xbuy[t] + xdischarge[t] == Edemand[t] + xcharge[t] + xsell[t]

        if t == 0:
            model += s[t] == s0 + charge_eff * xcharge[t] - xdischarge[t] / discharge_eff
        else:
            model += s[t] == s[t-1] + charge_eff * xcharge[t] - xdischarge[t] / discharge_eff

        model += xcharge[t] <= Pcharge_max * ycharge[t]
        model += xdischarge[t] <= Pdischarge_max * ydischarge[t]
        model += ycharge[t] + ydischarge[t] <= 1

        model += xbuy[t] <= Pbuy_max
        model += xsell[t] <= Psell_max


    model.solve(PULP_CBC_CMD(msg=False))

    # --- Extract results ---
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
        })
    df = pd.DataFrame(data)

    actual_cost = value(model.objective)
    exported = df["Sell"].sum()


    if not save_results:
        return {
            'exported': exported,
            'actual_cost': -actual_cost,
            'baseline_cost': baseline_cost
        }

    df.to_csv(f"{results_folder}/{scenario_name.replace(' ', '_')}_table.csv", index=False)

    print(f"\n{'=' * 60}")
    print(scenario_name)
    print(f"{'=' * 60}")
    print(df.round(2).to_string(index=False))
    print(f"-> Baseline Cost: {baseline_cost:.2f} AMD | Actual Cost: {actual_cost:.2f} AMD | Exported: {exported:.1f} kWh")

    # --- Plots ---
    charts.scenario_chart(df, actual_cost, exported, scenario_name, results_folder)
    charts.costs_chart(df, C_buy, C_sell, actual_cost, T, scenario_name, results_folder)
    charts.sources_chart(df, scenario_name, results_folder)
    charts.decision_variables_chart(df, scenario_name, results_folder)
    charts.battery_charging_chart(df, scenario_name, results_folder)

    return df