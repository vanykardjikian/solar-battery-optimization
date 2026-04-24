from gekko import GEKKO
import pandas as pd

import charts
from constants import (
    T, C_buy, E_solar, E_demand, E_cap,
    P_charge_max, P_discharge_max, charge_eff, discharge_eff, s0,
    P_buy_max, P_sell_max,
    k,
)


def solve_scenario(C_sell, scenario_name, results_folder, save_results=True):
    """Solve MINLP for one tariff scenario; returns DataFrame or dict if save_results=False."""
    baseline_cost = sum(C_buy[t] * E_demand[t] for t in T)
    m = GEKKO(remote=False)
    nt = 24

    x_buy = [m.Var(lb=0, ub=P_buy_max) for _ in range(nt)]
    x_sell = [m.Var(lb=0, ub=P_sell_max) for _ in range(nt)]
    x_charge = [m.Var(lb=0, ub=P_charge_max) for _ in range(nt)]
    x_discharge = [m.Var(lb=0, ub=P_discharge_max) for _ in range(nt)]
    s = [m.Var(lb=0, ub=E_cap) for _ in range(nt)]

    y_charge = [m.Var(lb=0, ub=1, integer=True) for _ in range(nt)]
    y_discharge = [m.Var(lb=0, ub=1, integer=True) for _ in range(nt)]


    m.Maximize(sum(C_sell[t]*x_sell[t] - C_buy[t]*x_buy[t] for t in range(nt)))

    # Energy balance
    for t in range(nt):
        m.Equation(E_solar[t] + x_buy[t] + x_discharge[t] == E_demand[t] + x_charge[t] + x_sell[t])

    for t in range(nt):
        loss = k * (x_charge[t]**2 / P_charge_max + x_discharge[t]**2 / P_discharge_max)
        if t == 0:
            m.Equation(s[t] == s0 + charge_eff*x_charge[t] - x_discharge[t]/discharge_eff - loss)
        else:
            m.Equation(s[t] == s[t-1] + charge_eff*x_charge[t] - x_discharge[t]/discharge_eff - loss)

    for t in range(nt):
        m.Equation(x_charge[t] <= P_charge_max * y_charge[t])
        m.Equation(x_discharge[t] <= P_discharge_max * y_discharge[t])
        m.Equation(x_buy[t] <= P_buy_max)
        m.Equation(x_sell[t] <= P_sell_max)

    for t in range(nt):
        m.Equation(y_charge[t] + y_discharge[t] <= 1)

    m.options.SOLVER = 1
    m.solve(disp=False)

    df = pd.DataFrame({
        "Hour": range(nt),
        "Solar": E_solar,
        "Demand": E_demand,
        "Buy": [round(x.value[0],3) for x in x_buy],
        "Sell": [round(x.value[0],3) for x in x_sell],
        "Charge": [round(x.value[0],3) for x in x_charge],
        "Discharge": [round(x.value[0],3) for x in x_discharge],
        "SOC": [round(x.value[0],2) for x in s],
        "y_c": [round(x.value[0],4) for x in y_charge],
        "y_d": [round(x.value[0],4) for x in y_discharge],
    })

    actual_cost = m.options.objfcnval
    exported = df["Sell"].sum()

    if not save_results:
        return {
            'exported': exported,
            'actual_cost': actual_cost,
            'baseline_cost': baseline_cost
    }

    df.to_csv(f"{results_folder}/{scenario_name.replace(' ', '_')}_table.csv", index=False)
    
    print(f"\n{'='*60}")
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
