import pandas as pd
from pulp import (PULP_CBC_CMD, LpBinary, LpMaximize, LpProblem, LpVariable,
                  value)

import charts
from constants import (C_buy, E_cap, E_demand, E_solar, P_buy_max,
                       P_charge_max, P_discharge_max, P_sell_max, T,
                       charge_eff, discharge_eff, s0)


def solve_scenario(C_sell, scenario_name, results_folder, save_results=True):
    """Solve MILP for one tariff scenario; returns DataFrame or dict if save_results=False."""
    baseline_cost = sum(C_buy[t] * E_demand[t] for t in T)

    model = LpProblem(f"Microgrid_{scenario_name}", LpMaximize)

    # --- Decision variables ---
    x_buy = LpVariable.dicts("xtbuy", T, 0, P_buy_max)
    x_sell = LpVariable.dicts("xtsell", T, 0, P_sell_max)
    x_charge = LpVariable.dicts("xtcharge", T, 0, P_charge_max)
    x_discharge = LpVariable.dicts("xtdischarge", T, 0, P_discharge_max)
    s = LpVariable.dicts("st", T, 0, E_cap)
    y_charge = LpVariable.dicts("ytcharge", T, cat=LpBinary)
    y_discharge = LpVariable.dicts("ytdischarge", T, cat=LpBinary)

    # --- Objective: maximize revenue from export minus grid purchase cost ---
    model += sum(C_sell[t] * x_sell[t] - C_buy[t] * x_buy[t] for t in T)

    # --- Constraints ---
    for t in T:
        model += (
            E_solar[t] + x_buy[t] + x_discharge[t]
            == E_demand[t] + x_charge[t] + x_sell[t]
        )

        if t == 0:
            model += (
                s[t] == s0 + charge_eff * x_charge[t] - x_discharge[t] / discharge_eff
            )
        else:
            model += (
                s[t]
                == s[t - 1] + charge_eff * x_charge[t] - x_discharge[t] / discharge_eff
            )

        model += x_charge[t] <= P_charge_max * y_charge[t]
        model += x_discharge[t] <= P_discharge_max * y_discharge[t]
        model += y_charge[t] + y_discharge[t] <= 1

        model += x_buy[t] <= P_buy_max
        model += x_sell[t] <= P_sell_max

    model.solve(PULP_CBC_CMD(msg=False))

    # --- Extract results ---
    data = []
    for t in T:
        data.append(
            {
                "Hour": t,
                "Solar": E_solar[t],
                "Demand": E_demand[t],
                "Buy": value(x_buy[t]),
                "Sell": value(x_sell[t]),
                "Charge": value(x_charge[t]),
                "Discharge": value(x_discharge[t]),
                "SOC": value(s[t]),
                "y_c": int(value(y_charge[t])),
                "y_d": int(value(y_discharge[t])),
            }
        )
    df = pd.DataFrame(data)

    actual_cost = value(model.objective)
    exported = df["Sell"].sum()

    if not save_results:
        return {
            "exported": exported,
            "actual_cost": -actual_cost,
            "baseline_cost": baseline_cost,
        }

    df.to_csv(
        f"{results_folder}/{scenario_name.replace(' ', '_')}_table.csv", index=False
    )

    print(f"\n{'=' * 60}")
    print(scenario_name)
    print(f"{'=' * 60}")
    print(df.round(2).to_string(index=False))
    print(
        f"-> Baseline Cost: {baseline_cost:.2f} AMD | Actual Cost: {actual_cost:.2f} AMD | Exported: {exported:.1f} kWh"
    )

    # --- Plots ---
    charts.scenario_chart(df, actual_cost, exported, scenario_name, results_folder)
    charts.costs_chart(df, C_buy, C_sell, actual_cost, T, scenario_name, results_folder)
    charts.sources_chart(df, scenario_name, results_folder)
    charts.decision_variables_chart(df, scenario_name, results_folder)
    charts.battery_charging_chart(df, scenario_name, results_folder)

    return df
