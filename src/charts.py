

from matplotlib import pyplot as plt
import numpy as np
from profiles import variable_tariff_profile


def solar_vs_demand(hour, solar, demand):
    """Plot 24h solar generation (bars) vs load demand (line)."""
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

def scenario_chart(df, actual_cost, exported, scenario_name, results_folder):
    """Plot hourly solar, demand, buy, sell, and SOC."""
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
    plt.savefig(f"{results_folder}/{scenario_name.replace(' ', '_')}.png", dpi=200)
    plt.close()


def costs_chart(df, C_buy, C_sell, actual_cost, T, scenario_name, results_folder):
    """Pie chart of grid purchase vs export revenue."""
    costs = {
    "Grid Purchase": sum(C_buy[t] * df["Buy"].iloc[t] for t in T),
    "Revenue from Export": sum(C_sell[t] * df["Sell"].iloc[t] for t in T),
    }
    plt.figure(figsize=(10,6))
    plt.pie([abs(v) for v in costs.values()], labels=costs.keys(), autopct='%1.1f%%', colors=['#e74c3c', '#27ae60'])
    plt.title(f"Cost Structure - {scenario_name} Net Cost: {actual_cost:.0f} AMD")
    plt.savefig(f"{results_folder}/{scenario_name.replace(' ', '_')}_costs.png", dpi=200)


def sources_chart(df, scenario_name, results_folder):
    """Stacked bar chart of solar, grid, battery supplying load."""
    plt.figure(figsize=(12, 6))

    solar_supply = df["Solar"].copy()
    grid_supply = df["Buy"].copy()
    battery_supply = df["Discharge"].copy()

    solar_supply = solar_supply.round(6)
    grid_supply = grid_supply.round(6)
    battery_supply = battery_supply.round(6)

    hours = df["Hour"]
    sources = [df["Solar"], df["Buy"], df["Discharge"]]
    colors = ["#f39c12", "#3498db", "#9b59b6"]
    labels = ["Solar PV", "Grid Import", "Battery Discharge"]

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
    plt.savefig(f"{results_folder}/{scenario_name.replace(' ', '_')}_sources.png", dpi=300)
    plt.close()

def decision_variables(df, scenario_name, results_folder):
    """Plot binary charge/discharge indicators."""
    _, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax[0].step(df["Hour"], df["y_c"], where='post', color='purple', linewidth=2)
    ax[0].set_yticks([0,1])
    ax[0].set_ylabel("Charge")
    ax[0].set_xlabel("Hour")
    ax[1].step(df["Hour"], df["y_d"], where='post', color='red', linewidth=2)
    ax[1].set_yticks([0,1])
    ax[1].set_ylabel("Discharge")
    ax[1].set_xlabel("Hour")
    plt.suptitle(f"{scenario_name} - Binary Decision Variables")
    plt.tight_layout()
    plt.savefig(f"{results_folder}/{scenario_name.replace(' ', '_')}_binary_decisions.png", dpi=300)


def battery_charging(df, scenario_name, results_folder):
    """Plot charge/discharge bars and SOC over time."""
    plt.figure(figsize=(11, 5))
    plt.bar(df["Hour"], df["Charge"], color='#27ae60', alpha=0.8, label="Charging (+)", width=0.8)
    plt.bar(df["Hour"], -df["Discharge"], color='#e74c3c', alpha=0.8, label="Discharging (-)", width=0.8)
    plt.axhline(0, color='black', linewidth=1.5)
    plt.plot(df["Hour"], df["SOC"], 'o-', color='#9b59b6', linewidth=3, markersize=6, label="SOC (kWh)", alpha=0.9)

    plt.title(f"{scenario_name} Battery Operation Strategy (Charge/Discharge + SOC)")
    plt.xlabel("Hour")
    plt.ylabel("Battery Power (kW)  /  SOC (kWh)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{results_folder}/{scenario_name.replace(' ', '_')}_battery_behavior.png", dpi=300)
    plt.close()


def plot_comparison(df_lin_A, df_lin_B, df_nonlin_A, df_nonlin_B):
    labels = [
        "Solar Generated",
        "Grid Import (Buy)",
        "Battery Discharge",
        "Energy Exported"
    ]

    lin_A = [df_lin_A["Solar"].sum(), df_lin_A["Buy"].sum(), df_lin_A["Discharge"].sum(), df_lin_A["Sell"].sum()]
    lin_B = [df_lin_B["Solar"].sum(), df_lin_B["Buy"].sum(), df_lin_B["Discharge"].sum(), df_lin_B["Sell"].sum()]
    nonlin_A = [df_nonlin_A["Solar"].sum(), df_nonlin_A["Buy"].sum(), df_nonlin_A["Discharge"].sum(), df_nonlin_A["Sell"].sum()]
    nonlin_B = [df_nonlin_B["Solar"].sum(), df_nonlin_B["Buy"].sum(), df_nonlin_B["Discharge"].sum(), df_nonlin_B["Sell"].sum()]

    x = np.arange(len(labels))
    width = 0.18

    _, ax = plt.subplots(figsize=(13, 8))
    ax.bar(x - 1.5 * width, lin_A, width, label="(Linear) - Scenario 1 - 22 AMD", color="#3498db", alpha=0.9)
    ax.bar(x - 0.5 * width, lin_B, width, label="(Linear) - Scenario 2 - 35/48 AMD", color="#04548a", alpha=0.9)
    ax.bar(x + 0.5 * width, nonlin_A, width, label="(Non-linear) - Scenario 1 - 22 AMD", color="#e74c3c", alpha=0.9)
    ax.bar(x + 1.5 * width, nonlin_B, width, label="(Non-linear) - Scenario 2 - 35/48 AMD", color="#ac2516", alpha=0.9)

    ax.set_ylabel("Energy (kWh)", fontsize=13)
    ax.set_title("Linear vs Non-linear Model Comparison", fontsize=16, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=12, fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.axhline(0, color='black', linewidth=0.8)

    plt.tight_layout()
    plt.savefig("results/comparison.png", dpi=300, bbox_inches='tight')
    plt.close()


def sensitivity_chart(solve_scenario, scenario_name, results_folder):
    """Sweep sell price 22-51 AMD/kWh and plot exported energy vs cost."""
    exports, actual_costs = [], []
    prices = range(22, 52, 1)
    for p in prices:
        low_price = min(22, p-14)
        price_profile = variable_tariff_profile(low_price, p)
        results = solve_scenario(price_profile, "", results_folder, False)
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
    plt.title(f"{scenario_name} Sensitivity Analysis: Sell Price Impact")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{results_folder}/{scenario_name}_sensitivity_analysis.png", dpi=250)
    plt.close()