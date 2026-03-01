T = range(24)

# Grid buy price (AMD/kWh): off-peak 0–6, peak 7–22, off-peak 23
C_buy = [38] * 7 + [52] * 16 + [38]

# Solar generation (kW) and load demand (kW) per hour
Esolar = [0] * 7 + [1, 4, 10, 18, 28, 36, 40, 41, 38, 32, 22, 12, 5, 2] + [0] * 3
Edemand = [5, 5, 5, 5, 5, 5, 10, 10, 25, 25, 25, 25, 20, 20, 30, 30, 30, 30, 15, 15, 8, 8, 8, 8]

# Battery: capacity (kWh), max charge/discharge (kW), round-trip efficiencies, initial SOC (kWh)
Ecap = 30
Pcharge_max = 12
Pdischarge_max = 12
charge_eff = 0.95
discharge_eff = 0.95
s0 = 15

# Grid limits (kW)
Pbuy_max = 60
Psell_max = 30

