# `src/profiles.py`

## Purpose

Defines helper function for constructing 24-hour export price  profiles used as input to the optimization models.

## main function

### `variable_tariff_profile(off_peak_price, peak_price)`

Returns a list `C_sell[t]` (AMD/kWh) of length 24:

- hours **0–6** and **23** -> `off_peak_price`
- hours **7–22** -> `peak_price`

## Examples:

- **Scenario 1**: `variable_tariff_profile(22, 22)` (flat export price)
- **Scenario 2**: `variable_tariff_profile(35, 48)` (off-peak / peak export price)
