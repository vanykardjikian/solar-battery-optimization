def variable_tariff_profile(off_peak_price, peak_price):
    return (
        [off_peak_price] * 7
        + [peak_price] * 16
        + [off_peak_price]
    )

