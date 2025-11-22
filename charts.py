

from matplotlib import pyplot as plt

def solar_vs_demand(hour, solar, demand):
    _, ax = plt.subplots(figsize=(11, 5))

    ax.bar(hour, solar, color='#f39c12', alpha=0.7, label="Solar Generation", width=0.9)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Solar Power (kW)")

    ax.plot(hour, demand, 's-', color='#e74c3c', linewidth=3, label="Demand")
    ax.set_ylabel("Demand (kW)")

    plt.title("Solar Generation vs Load Demand Profile (24h)")
    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc="upper left")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("results/solar_vs_demand.png", dpi=300)
    plt.close()

def scenario_chart(df, actual_cost, exported, scenario_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df["Hour"], df["Solar"], label="Solar", marker='o')
    plt.plot(df["Hour"], df["Demand"], label="Demand", marker='s')
    plt.plot(df["Hour"], df["Buy"], label="Buy", linestyle='--')
    plt.plot(df["Hour"], df["Sell"], label="Sell", linestyle='-.')
    plt.fill_between(df["Hour"], 0, df["SOC"], alpha=0.3, label="SOC")
    plt.title(f"{scenario_name}\nExport: {exported:.1f} kWh | Actual Cost: {actual_cost:.0f} AMD")
    plt.xlabel("Hour")
    plt.ylabel("kWh")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"results/{scenario_name.replace(' ', '_')}.png", dpi=200)
    plt.close()


def costs_chart(df, C_buy, export_price, actual_cost, T, scenario_name):
    costs = {
    "Grid Purchase": sum(C_buy[t] * df["Buy"].iloc[t] for t in T),
    "Revenue from Export": sum(export_price * df["Sell"].iloc[t] for t in T),
    }
    plt.figure(figsize=(10,6))
    plt.pie([abs(v) for v in costs.values()], labels=costs.keys(), autopct='%1.1f%%', colors=['#e74c3c', '#27ae60'])
    plt.title(f"Cost Structure - {scenario_name} Export Price {export_price} AMD/kWh\nNet Cost: {actual_cost:.0f} AMD")
    plt.savefig(f"results/{scenario_name.replace(' ', '_')}_costs.png", dpi=200)


def sources_chart(df, scenario_name):
    plt.figure(figsize=(12, 6))

    solar_supply   = df["Solar"].copy()
    grid_supply    = df["Buy"].copy()
    battery_supply = df["Discharge"].copy()

    solar_supply   = solar_supply.round(6)
    grid_supply    = grid_supply.round(6)
    battery_supply = battery_supply.round(6)

    hours = df["Hour"]
    sources = [df["Solar"], df["Buy"], df["Discharge"]]
    colors  = ["#f39c12", "#3498db", "#9b59b6"]
    labels  = ["Solar PV", "Grid Import", "Battery Discharge"]

    bottom = 0
    for data, color, label in zip(sources, colors, labels):
        plt.bar(hours, data, bottom=bottom, label=label, color=color, alpha=0.9)
        bottom += data

    plt.plot(hours, df["Demand"], 'k-', linewidth=3, marker='o', markersize=4, label="Demand")

    plt.title(f"{scenario_name} - Energy Sources Supplying the Load (24h)", fontsize=14, pad=20)
    plt.xlabel("Hour of Day")
    plt.ylabel("Power (kW)")
    plt.legend(loc="upper left")
    plt.grid(alpha=0.3, axis='y')
    plt.xticks(range(0, 24, 1))
    plt.tight_layout()
    plt.savefig(f"results/{scenario_name.replace(' ', '_')}_sources.png", dpi=300)
    plt.close()

def decision_variables(df, scenario_name):
    _, ax = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    ax[0].step(df["Hour"], df["y_b"], where='post', color='blue', linewidth=2)
    ax[0].set_yticks([0,1])
    ax[0].set_ylabel("Buy")
    ax[1].step(df["Hour"], df["y_s"], where='post', color='green', linewidth=2)
    ax[1].set_yticks([0,1])
    ax[1].set_ylabel("Sell")
    ax[2].step(df["Hour"], df["y_c"], where='post', color='purple', linewidth=2)
    ax[2].set_yticks([0,1])
    ax[2].set_ylabel("Charge")
    ax[3].step(df["Hour"], df["y_d"], where='post', color='red', linewidth=2)
    ax[3].set_yticks([0,1])
    ax[3].set_ylabel("Discharge")
    ax[3].set_xlabel("Hour")
    plt.suptitle("Binary Decision Variables (MILP Control Signals)")
    plt.tight_layout()
    plt.savefig(f"results/{scenario_name.replace(' ', '_')}_binary_decisions.png", dpi=300)


def battery_charging(df, scenario_name):
    plt.figure(figsize=(11, 5))
    plt.bar(df["Hour"], df["Charge"], color='#27ae60', alpha=0.8, label="Charging (+)", width=0.8)
    plt.bar(df["Hour"], -df["Discharge"], color='#e74c3c', alpha=0.8, label="Discharging (-)", width=0.8)
    plt.axhline(0, color='black', linewidth=1.5)
    plt.plot(df["Hour"], df["SOC"], 'o-', color='#9b59b6', linewidth=3, markersize=6, label="SOC (kWh)", alpha=0.9)

    plt.title("Battery Operation Strategy (Charge/Discharge + SOC)")
    plt.xlabel("Hour")
    plt.ylabel("Battery Power (kW)  /  SOC (kWh)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"results/{scenario_name.replace(' ', '_')}_battery_behavior.png", dpi=300)
    plt.close()


def plot_comparison(scenario1_data, scenario2_data):
    s1 = scenario1_data
    s2 = scenario2_data

    labels = [
        "Solar Generated",
        "Grid Import (Buy)",
        "Battery Discharge",
        "Energy Exported",
    ]

    val_s1 = [sum(s1["Solar"]), sum(s1["Buy"]), sum(s1["Discharge"]), sum(s1["Sell"])]
    val_s2 = [sum(s2["Solar"]), sum(s2["Buy"]), sum(s2["Discharge"]), sum(s2["Sell"])]

    x = range(len(labels))
    width = 0.35

    _, ax = plt.subplots(figsize=(12, 7))

    ax.bar([i - width/2 for i in x], val_s1, width, 
                   label="Scenario 1 - 22 AMD/kWh", color="#3498db", alpha=0.9)
    ax.bar([i + width/2 for i in x], val_s2, width, 
                   label="Scenario 2 - 48 AMD/kWh", color="#e74c3c", alpha=0.9)

    ax.set_ylabel("Energy (kWh)", fontsize=12)
    ax.set_title("Comparison: Export Price Impact (22 vs 48 AMD/kWh)", fontsize=15, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.axhline(0, color='black', linewidth=0.8)

    plt.tight_layout()
    plt.savefig("results/comparison_both_scenarios.png", dpi=300, bbox_inches='tight')
    plt.close()


def sensitivity_chart(solve_scenario):
    exports, actual_costs, = [], []
    prices = range(15, 71, 5)
    for p in prices:
        results = solve_scenario(p, f"Sens_{p}AMD", False)
        exp = results['exported']
        cost = results['actual_cost']
        baseline_cost = results['baseline_cost']
        exports.append(exp)
        actual_costs.append(cost)

    plt.figure(figsize=(10, 5))
    plt.plot(prices, exports, 'o-', color="green", label="Exported Energy (kWh)")
    plt.plot(prices, [pr/1000 for pr in actual_costs], 's-', color="purple", label="Actual Cost (thousands AMD)")
    plt.plot(prices, [baseline_cost/1000 for _ in prices], linewidth=2, linestyle='--', color="black", label="Baseline Cost (thousands AMD)")
    plt.axvline(x=22, color='#c0392b', linewidth=2, linestyle='--', label='Current sell price (22 AMD/kWh)')
    plt.xlabel("Price (AMD/kWh)")
    plt.ylabel("kWh / thousand AMD")
    plt.title("Sensitivity Analysis: Sell Price Impact")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("results/sensitivity_analysis.png", dpi=250)
    plt.close()