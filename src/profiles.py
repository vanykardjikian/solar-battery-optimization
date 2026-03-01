def variable_tariff_profile(off_peak_price, peak_price):
    """Build 24h sell-price profile (AMD/kWh): off-peak for hours 0-6 and 23, peak for 7-22."""
    return [off_peak_price] * 7 + [peak_price] * 16 + [off_peak_price]

