def calculate_quantity(entry, stop_loss, capital, risk_percent):
    risk_amount = capital * (risk_percent / 100)
    risk_per_unit = abs(entry - stop_loss)
    qty = int(risk_amount / risk_per_unit) if risk_per_unit != 0 else 0
    return qty
