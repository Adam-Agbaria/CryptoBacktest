from constants.parameters import same_tp_all, same_sl_all





def check_ema_crossover(intraday_data, lines, invalidated_lines, daily_date, trend, ema_period=21):
    """
    Check if the intraday price hits the 21 EMA from above or below.

    Parameters:
    intraday_row (DataFrame row): The current row of intraday data.
    lines (dict): Contains various support/resistance lines including EMA.
    invalidated_lines (dict): Lines that have been invalidated.
    daily_date (date): The date of the current processing day.
    ema_period (int): Period for the EMA calculation. Default is 21.

    Returns:
    dict: A dictionary with crossover information or None if no crossover.
    """
    trade = None
    ema = lines['EMA100']
    prev_close = lines['prev_close']

    # Check if EMA exists for the day
    if ema is None:
        return None

    hit_ema_from_below = (intraday_data['high'] >= ema) and (prev_close < ema) and (ema not in invalidated_lines.get(daily_date, []))
    hit_ema_from_above = (intraday_data['low'] <= ema) and (prev_close > ema) and (ema not in invalidated_lines.get(daily_date, []))
    entry_price = ema
    if hit_ema_from_below:
        condition = 'hit_ema_from_below'
        trade = ema_trigger_logic(intraday_data, lines, invalidated_lines, daily_date, condition, trend, entry_price)
        return trade
    elif hit_ema_from_above:
        condition = 'hit_ema_from_above'
        trade = ema_trigger_logic(intraday_data, lines, invalidated_lines, daily_date, condition, trend, entry_price)

        return trade

    return trade

def ema_trigger_logic(intraday_data, lines, invalidated_lines, daily_date, condition, trend, entry_price):
    # Logic for handling different conditions based on the trend and specific condition
    position = None
    current_time = intraday_data.name.time().strftime('%H:%M')  # Get the time component
    current_date = intraday_data.name.date()  # Get the date component
    trade = None

    if condition == 'hit_ema_from_below':

        if trend == "Neutral":
            entry_price = entry_price
            position = 'SELL'
            tp = entry_price * same_tp_all
            sl = entry_price * same_sl_all
            trade = { 
            'position': position,
            'tp': tp,  
            'sl': sl,
            'entry_price': entry_price,
            'entry_time': current_time,
            'entry_date': current_date, 
            'entry_date': current_date, 
            'trade_trigger': 'hit_ema_from_below Neutral'
            }
            print(f"{position} position triggered EMA at {current_date} {current_time} during {trend} trend")
            return trade
    if condition == 'hit_ema_from_above':
        if trend == "Neutral":
            entry_price = entry_price
            position = 'BUY'
            tp = entry_price * same_tp_all
            sl = entry_price * same_sl_all
            trade = { 
            'position': position,
            'tp': tp,  
            'sl': sl,
            'entry_price': entry_price,
            'entry_time': current_time,
            'entry_date': current_date, 
            'entry_date': current_date, 
            'trade_trigger': 'hit_ema_from_above Neutral'
            }
            print(f"{position} position triggered EMA at {current_date} {current_time} during {trend} trend")
            return trade

    return None

def terminate_trade(trade, intraday_data, intraday_index, lines, daily_date, invalidated_lines):
    lines['high'] = round(lines['high'], 4)
    lines['low'] = round(lines['low'], 4)
    lines['mid'] = round(lines['mid'], 4)
    lines['c0_236'] = round(lines['c0_236'], 4)
    lines['c0_786'] = round(lines['c0_786'], 4)
    if not trade:
        return None, "No active trade"
    current_price = intraday_data['close']
    candle_low = intraday_data['low']
    candle_high = intraday_data['high']

    position = trade['position']
    entry_price = trade['entry_price']
    entry_time = trade['entry_time']

    current_time = intraday_index.strftime('%H:%M')

    tp = trade['tp']
    sl = trade['sl']

    # Calculating the SL and TP prices
    sl_price = entry_price - sl if position == 'BUY' else entry_price + sl
    tp_price = entry_price + tp if position == 'BUY' else entry_price - tp

    sl_price = round(sl_price,3)
    tp_price = round(tp_price,3)

    # Check if SL or TP is hit
    trade_terminated = False
    points_gained = 0
    # print(f"Current price: {current_price}, SL: {sl_price}, TP: {tp_price}")


    if position == 'BUY':
        if candle_low <= sl_price:
            trade_terminated = True
            points_gained = sl_price - entry_price  # Loss
            invalidated_lines.setdefault(daily_date, []).append(entry_price)
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {sl_price} Profit: {points_gained}\n")
            position = None
        elif candle_high >= tp_price:
            trade_terminated = True
            points_gained = tp_price - entry_price  # Profit
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {tp_price} Profit: {points_gained}\n")
            position = None
    elif position == 'SELL':
        if candle_high >= sl_price:
            trade_terminated = True
            points_gained = entry_price - sl_price  # Loss
            invalidated_lines.setdefault(daily_date, []).append(entry_price)
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {sl_price} Profit: {points_gained}\n")
            position = None
        elif candle_low <= tp_price:
            trade_terminated = True
            points_gained = entry_price - tp_price  # Profit
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {tp_price} Profit: {points_gained}\n")
            position = None

    # print(f"Checking termination for trade entered on {trade['entry_time']}, current time: {intraday_index}")

    status = "Terminated" if trade_terminated else "Active"
    return points_gained, status, trade




