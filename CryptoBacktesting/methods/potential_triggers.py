import sys
sys.path.append('..')
from constants.parameters import same_tp_all, same_sl_all

def check_potential_trigger(intraday_data, lines, invalidated_lines, daily_date, trend):

    """
    We check for a potential trade trigger and execute in case we find a trigger.
    Here we use a simple strategy of initiating trades in condition of a suitable
    market trend and price. The proposed prices are Fibonaci lines where the High is
    the previous day High and the Low is the previous day Low
    """

    hit_high_from_below = ((intraday_data['high'] >= lines['high']) & (lines['prev_close'] < lines['high']) & (lines['high'] not in invalidated_lines.get(daily_date, [])))
    hit_low_from_above = ((intraday_data['low'] <= lines['low']) & (lines['prev_close'] > lines['low']) & (lines['low'] not in invalidated_lines.get(daily_date, [])))
    hit_mid_from_above = ((intraday_data['low'] <= lines['mid']) & (lines['prev_close'] > lines['mid']) & (lines['mid'] not in invalidated_lines.get(daily_date, [])))
    hit_mid_from_below = ((intraday_data['high'] >= lines['mid']) & (lines['prev_close'] < lines['mid']) & (lines['mid'] not in invalidated_lines.get(daily_date, [])))

    hit_fibo_0_236_from_above = ((intraday_data['low'] <= lines['c0_236'])  & (lines['prev_close'] > lines['c0_236']) & (lines['c0_236'] not in invalidated_lines.get(daily_date, [])))
    hit_fibo_0_236_from_below = ((intraday_data['high'] >= lines['c0_236']) & (lines['prev_close'] < lines['c0_236']) & (lines['c0_236'] not in invalidated_lines.get(daily_date, [])))
    hit_fibo_0_786_from_above = ((intraday_data['low'] <= lines['c0_786'])  & (lines['prev_close'] > lines['c0_786']) & (lines['c0_786'] not in invalidated_lines.get(daily_date, [])))
    hit_fibo_0_786_from_below = ((intraday_data['high'] >= lines['c0_786']) & (lines['prev_close'] < lines['c0_786']) & (lines['c0_786'] not in invalidated_lines.get(daily_date, [])))
    
    trade = None
    # Handling for each scenario
    if hit_high_from_below:
        condition = 'hit_high_from_below'
        trade =  trigger_logic(intraday_data, condition, trend, lines['high'])

    elif hit_low_from_above:
        condition = 'hit_low_from_above'
        trade =  trigger_logic(intraday_data,  condition, trend, lines['low'])
        return trade
    
    elif hit_mid_from_above:
        condition = 'hit_mid_from_above'
        trade =  trigger_logic(intraday_data,  condition, trend, lines['mid'])
        return trade

    elif hit_mid_from_below:
        condition = 'hit_mid_from_below'
        trade =  trigger_logic(intraday_data,  condition, trend,lines['mid'])
        return trade
    
    elif hit_fibo_0_236_from_above:
        condition = 'hit_fibo_0_236_from_above'
        trade =  trigger_logic(intraday_data,  condition, trend, lines['c0_236'])
        return trade
    
    elif hit_fibo_0_236_from_below:
        condition = 'hit_fibo_0_236_from_below'
        trade =  trigger_logic(intraday_data,  condition, trend, lines['c0_236'])
        return trade
    
    elif hit_fibo_0_786_from_above:
        condition = 'hit_fibo_0_786_from_above'
        trade =  trigger_logic(intraday_data,  condition, trend, lines['c0_786'])
        return trade
    
    elif hit_fibo_0_786_from_below:
        condition = 'hit_fibo_0_786_from_below'
        trade =  trigger_logic(intraday_data,  condition, trend, lines['c0_786'])
        return trade

    return trade

def trigger_logic(intraday_data, condition, trend, entry_price):
    """
    For each price trigger we execute a trade while the direction of the trade will be dependent on
    the current market Trend.
    """

    # Logic for handling different conditions based on the trend and specific condition
    position = None
    current_time = intraday_data.name.time().strftime('%H:%M')  # Get the time component
    current_date = intraday_data.name.date()  # Get the date component
    trade = None
    if condition == 'hit_high_from_below':

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
            'trade_trigger': 'hit_high_from_below Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade
        if trend == "Bullish":
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
            'trade_trigger': 'hit_high_from_below Bullish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        if trend == "Bearish":
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
            'trade_trigger': 'hit_high_from_below Bearish'
            }

            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

    if condition == 'hit_low_from_above':  

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
            'trade_trigger': 'hit_low_from_above Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        

        if trend == "Bearish":
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
            'trade_trigger': 'hit_low_from_above Bearish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

    if condition == 'hit_mid_from_above':

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
            'trade_trigger': 'hit_mid_from_above Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        if trend == "Bullish": 
              #just now
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
            'trade_trigger': 'hit_mid_from_above Bullish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        if trend == "Bearish": 
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
            'trade_trigger': 'hit_mid_from_above Bearish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

    if condition == 'hit_mid_from_below':

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
            'trade_trigger': 'hit_mid_from_below Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        
        if trend == "Bearish": 
            #just now
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
            'trade_trigger': 'hit_mid_from_below Bearish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

    if condition == 'hit_fibo_0_236_from_above': 

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
            'trade_trigger': 'hit_fibo_0_236_from_above Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        

        if trend == "Bearish": 
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
            'trade_trigger': 'hit_fibo_0_236_from_above Bearish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

    if condition == 'hit_fibo_0_236_from_below': 

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
            'trade_trigger': 'hit_fibo_0_236_from_below Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        

        

    if condition == 'hit_fibo_0_786_from_above':

        if trend == "Neutral": #Non profitable
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
            'trade_trigger': 'hit_fibo_0_786_from_above Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        if trend == "Bullish": 
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
            'trade_trigger': 'hit_fibo_0_786_from_above Bullish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        if trend == "Bearish": 
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
            'trade_trigger': 'hit_fibo_0_786_from_above Bearish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

    if condition == 'hit_fibo_0_786_from_below': 

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
            'trade_trigger': 'hit_fibo_0_786_from_below Neutral'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        if trend == "Bullish": 
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
            'trade_trigger': 'hit_fibo_0_786_from_below Bullish'
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

        if trend == "Bearish":
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
            'trade_trigger': 'hit_fibo_0_786_from_below Bearish'
            
            }
            print(f"{position} position triggered at {current_date} {current_time} during {trend} trend")
            return trade

def terminate_trade(trade, intraday_data, intraday_index, lines, daily_date, invalidated_lines):
    """
    We check if the current price reached the TP or the SL.
    In case it does we terminate the trade
    """
    
    if not trade:
        return None, "No active trade"
    
    current_price = intraday_data['close']
    candle_low = intraday_data['low']
    candle_high = intraday_data['high']

    position = trade['position']
    entry_price = trade['entry_price']

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


    if position == 'BUY':
        if candle_low <= sl_price:
            if trade['entry_time'] == current_time:
                #This condition ensures that the trade candle isn't 
                #the one we executed the trade at. We Cancel those 
                #trades from the backtesting because to handle such senarios 
                #we need ticks data that we currently don't have
                
                print("Trade Deleted")
                status = "Terminated"
                position = None
                return points_gained, status, trade
            trade_terminated = True
            points_gained = sl_price - entry_price  # Loss
            invalidated_lines.setdefault(daily_date, []).append(entry_price)
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {sl_price} Profit: {points_gained}\n")
            position = None
        elif candle_high >= tp_price:
            if trade['entry_time'] == current_time:
                print("Trade Deleted")
                status = "Terminated"
                position = None
                return points_gained, status, trade
            trade_terminated = True
            points_gained = tp_price - entry_price  # Profit
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {tp_price} Profit: {points_gained}\n")
            position = None
    elif position == 'SELL':
        if candle_high >= sl_price:
            if trade['entry_time'] == current_time:
                print("Trade Deleted")
                status = "Terminated"
                position = None
                return points_gained, status, trade
            trade_terminated = True
            points_gained = entry_price - sl_price  # Loss
            invalidated_lines.setdefault(daily_date, []).append(entry_price)
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {sl_price} Profit: {points_gained}\n")
            position = None
        elif candle_low <= tp_price:
            if trade['entry_time'] == current_time:
                print("Trade Deleted")
                status = "Terminated"
                position = None
                return points_gained, status, trade
            trade_terminated = True
            points_gained = entry_price - tp_price  # Profit
            print(f"{position} position terminated at {current_time} Prices: {entry_price} -> {tp_price} Profit: {points_gained}\n")
            position = None


    status = "Terminated" if trade_terminated else "Active"
    return points_gained, status, trade




