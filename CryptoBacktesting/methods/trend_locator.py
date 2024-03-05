def determine_trend(lines):
    """
    Determining the market Trend based on the previous day RSI level.
    """
    trend = 'Neutral'
    if lines['daily_rsi'] is None:
        return trend
    if(lines['daily_rsi'] != None):
        if(lines['daily_rsi'] >= 70):
            trend = 'Bullish'
        elif(lines['daily_rsi'] <= 30):
            trend = 'Bearish'
        else:
            trend = 'Neutral'
    else:
        return trend
    return trend
    
def calculate_previous_levels(df):
    """
    This function determines the High,Low,Mid Fibo, 0.236 Fibo and 0.786 Fibo 
    of the previous day.
    """
    df['prev_high'] = df['high'].shift()
    df['prev_low'] = df['low'].shift()
    df['prev_mid'] = (df['prev_high'] + df['prev_low']) / 2
    df['prev_0.236'] = df['prev_low'] + 0.236 * (df['prev_high'] - df['prev_low'])
    df['prev_0.786'] = df['prev_low'] + 0.786 * (df['prev_high'] - df['prev_low'])
    return df

def extract_lines_from_day_row(day_row):
    """
    We insert the data of the sent row in a dictionary to have the data concentrated in
    one parameter.
    """
    day_row['prev_high'] = round(day_row['prev_high'],3)
    day_row['prev_low'] = round(day_row['prev_low'],3)
    day_row['prev_mid'] = round(day_row['prev_mid'],3)
    day_row['prev_0.236'] = round(day_row['prev_0.236'],3)
    day_row['prev_0.786'] = round(day_row['prev_0.786'],3)

    lines = {
        'high': day_row['prev_high'],
        'low': day_row['prev_low'],  
        'mid': day_row['prev_mid'],
        'c0_236': day_row['prev_0.236'],
        'c0_786': day_row['prev_0.786'],
    }
    return lines


