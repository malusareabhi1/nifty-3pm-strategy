import time
from datetime import datetime
from broker.zerodha import get_ltp, place_order
from strategy.breakout_logic import generate_breakout_levels
from strategy.capital_manager import calculate_quantity
from utils.alerts import send_telegram

def run_live_breakout(threepm_high, threepm_low, capital, risk_pct, offset=100):
    entry, sl, target = generate_breakout_levels(threepm_high, threepm_low, offset)
    qty = calculate_quantity(entry, sl, capital, risk_pct)

    print(f"🎯 Watching for breakout at ₹{entry}, SL: ₹{sl}, Qty: {qty}")

    while True:
        price = get_ltp("NIFTY 50")
        if price:
            print(f"{datetime.now().strftime('%H:%M:%S')} – LTP: ₹{price}")
            if price >= entry:
                order_id = place_order("NIFTY23AUG17600CE", qty=qty)
                send_telegram(f"🚀 Breakout triggered at ₹{price}, Order ID: {order_id}")
                break
        time.sleep(30)
