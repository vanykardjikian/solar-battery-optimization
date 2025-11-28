from gekko import GEKKO
import pandas as pd
import charts
from constants import (
    T,
    C_buy,
    Esolar,
    Edemand,
    Ecap,
    Pcharge_max,
    Pdischarge_max,
    charge_eff,
    discharge_eff,
    s0,
    Pbuy_max,
    Psell_max,
)

def solve_scenario(C_sell, scenario_name, results_folder, save_results = True):
    baseline_cost = sum(C_buy[t] * Edemand[t] for t in T)
    m = GEKKO(remote=False)
    nt = 24

    buy  = [m.Var(lb=0, ub=Pbuy_max) for _ in range(nt)]
    sell = [m.Var(lb=0, ub=Psell_max) for _ in range(nt)]
    ch   = [m.Var(lb=0, ub=Pcharge_max) for _ in range(nt)]
    dis  = [m.Var(lb=0, ub=Pdischarge_max) for _ in range(nt)]
    soc  = [m.Var(lb=0, ub=Ecap) for _ in range(nt)]

    yc = [m.Var(lb=0, ub=1, integer=True) for _ in range(nt)]
    yd = [m.Var(lb=0, ub=1, integer=True) for _ in range(nt)]


    m.Maximize(sum(C_sell[t]*sell[t] - C_buy[t]*buy[t] for t in range(nt)))

    # Energy balance
    for t in range(nt):
        m.Equation(Esolar[t] + buy[t] + dis[t] == Edemand[t] + ch[t] + sell[t])

    k = 0.012
    for t in range(nt):
        loss = k * (ch[t]**2 / Pcharge_max + dis[t]**2 / Pdischarge_max)
        if t == 0:
            m.Equation(soc[t] == s0 + charge_eff*ch[t] - dis[t]/discharge_eff - loss)
        else:
            m.Equation(soc[t] == soc[t-1] + charge_eff*ch[t] - dis[t]/discharge_eff - loss)

    for t in range(nt):
        m.Equation(ch[t]  <= Pcharge_max    * yc[t])
        m.Equation(dis[t] <= Pdischarge_max * yd[t])
        m.Equation(buy[t] <= Pbuy_max)
        m.Equation(sell[t]<= Psell_max)

    for t in range(nt):
        m.Equation(yc[t] + yd[t] <= 1)

    m.options.SOLVER = 1
    m.solve(disp=False)

    df = pd.DataFrame({
        "Hour": range(nt),
        "Solar": Esolar,
        "Demand": Edemand,
        "Buy": [round(x.value[0],3) for x in buy],
        "Sell": [round(x.value[0],3) for x in sell],
        "Charge": [round(x.value[0],3) for x in ch],
        "Discharge": [round(x.value[0],3) for x in dis],
        "SOC": [round(x.value[0],2) for x in soc],
        "y_c": [round(x.value[0],4) for x in yc],
        "y_d": [round(x.value[0],4) for x in yd],
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
    print(f"{'='*60}")
    print(df.round(2).to_string(index=False))
    print(f"→ Baseline Cost: {baseline_cost:.2f} AMD | Actual Cost: {actual_cost:.2f} AMD | Exported: {exported:.1f} kWh")

    # === Plots ===
    charts.scenario_chart(df, m.options.objfcnval, 55, scenario_name, results_folder)
    charts.costs_chart(df, C_buy, C_sell, m.options.objfcnval, T, scenario_name, results_folder)
    charts.sources_chart(df, scenario_name, results_folder)
    charts.decision_variables(df, scenario_name, results_folder)
    charts.battery_charging(df, scenario_name, results_folder)

    return df
