# Microgrid Optimization Using Linear Programming   

This repository contains an implementation of a **microgrid energy scheduling optimization model** using **Mixed Integer Linear Programming (MILP)** with **Python + PuLP + CBC solver**.  
The goal is to minimize the operational cost of a grid-connected building with:
- photovoltaic solar generation  
- a battery storage system  
- the ability to buy energy from the grid and sell excess electricity  

---

## **Problem Description**

We consider a 24-hour operation of a building equipped with:
- Solar PV generation
- Battery storage (charging/discharging efficiency included)
- Grid connection (buy & sell)
- Hourly demand profile

The objective is to **minimize the electricity cost**, or equivalently **maximize the profit**, while obeying:
- power balance
- storage capacity
- charge/discharge limits
- binary charging vs discharging decisions
- binary buying vs selling decisions
- grid buy/sell constraints

---

## **Model Summary**

## What the model does
- Mixed-Integer Linear Program (MILP) solved with PuLP + CBC
- Two scenarios:

| Scenario                      | Export price |
|-------------------------------|--------------|
| 1 - Current tarrif | 22 AMD/kWh   |
| 2 - Hypothetical   | 48 AMD/kWh   |

- Charts for visualization


### **Decision Variables**
- `xtbuy[t]` – grid energy purchased  
- `xtsell[t]` – energy sold to grid  
- `xtcharge[t]` – battery charging energy  
- `xtdischarge[t]` – battery discharging energy  
- `st[t]` – battery state of charge  

Binary variables:
- `ytcharge[t]`, `ytdischarge[t]` – avoid charging & discharging at hour
- `ytbuy[t]`, `ytsell[t]` – avoid buy & sell same hour  

---

## **Technology Stack**
- Python 3
- PuLP (MILP modelling)
- Pandas
- Matplotlib (via charts.py)

---

**Repository Structure**

- charts.py (All visualization utilities)

- main.py  (Main optimization code)

- results/ (Generated plots and tables)

- README.md (Documentation)

---

## **How to Run**

### Install dependencies
```bash
pip install pulp pandas matplotlib
```

### Run the optimization script
```bash 
python main.py
```

### View results

All output tables & charts will appear in:

```bash 
/results
```

## License

MIT License.



