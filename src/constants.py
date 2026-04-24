T = range(24)

# Grid buy price (AMD/kWh): off-peak 0–6, peak 7–22, off-peak 23
C_buy = [38] * 7 + [52] * 16 + [38]

# Solar generation (kW) and load demand (kW) per hour
E_solar = [0] * 7 + [1, 4, 10, 18, 28, 36, 40, 41, 38, 32, 22, 12, 5, 2] + [0] * 3
E_demand = [5, 5, 5, 5, 5, 5, 10, 10, 25, 25, 25, 25, 20, 20, 30, 30, 30, 30, 15, 15, 8, 8, 8, 8]

# Battery: capacity (kWh), max charge/discharge (kW), round-trip efficiencies, initial SOC (kWh)
E_cap = 30
P_charge_max = 12
P_discharge_max = 12
charge_eff = 0.95
discharge_eff = 0.95
s0 = 15

# Grid limits (kW)
P_buy_max = 60
P_sell_max = 30

# Loss coefficient
k = 0.012

