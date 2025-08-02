def generate_breakout_levels(threepm_high, threepm_low, offset=100):
    entry = threepm_high + offset
    sl = threepm_low
    target = entry + (entry - sl) * 1.5
    return entry, sl, target

def generate_breakdown_levels(threepm_close, threepm_high, offset=100):
    entry = threepm_close
    sl = threepm_high
    target = entry - (sl - entry) * 1.5
    return entry, sl, target
