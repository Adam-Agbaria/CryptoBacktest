from datetime import datetime
import pandas as pd


def get_week_number(date):
    """
    Function to get the week number and year. Used to print the weekly profits
    """
    return date.isocalendar()[0], date.isocalendar()[1]  # Year, Week number

def get_last_weeks_rsi(weekly_data, current_date):
    """
    Function to get the previous week RSI.
    """
    last_week_date = current_date - pd.DateOffset(weeks=1)
    last_week_data = weekly_data[weekly_data.index <= last_week_date]
    if not last_week_data.empty:
        return last_week_data.iloc[-1]['rsi']
    else:
        return None

def get_yesterdays_rsi(daily_data, current_date):
    """
    Function to get the previous day RSI.
    """
    yesterday = current_date - pd.DateOffset(days=1)
    if yesterday in daily_data.index:
        return daily_data.loc[yesterday, 'rsi']
    else:
        return None

def get_previous_1m_candle_rsi(intraday_data, current_timestamp):
    """
    Function to get the previous minute RSI.
    """
    previous_candle_timestamp = current_timestamp - pd.DateOffset(minutes=1)
    if previous_candle_timestamp in intraday_data.index:
        return intraday_data.loc[previous_candle_timestamp, 'rsi']
    else:
        return None
    
def compute_rma(data, window):
    """
    Function that helps calculating the RSI..
    """
    alpha = 1 / window
    return data.ewm(alpha=alpha, min_periods=window, adjust=False).mean()

def compute_rsi(data, window=14):
    """
    Function that calculated the RSI. We used it to add to the csv data for each candle
    the RSI levels.
    """
    change = data.diff()
    gain = change.where(change > 0, 0)
    loss = -change.where(change < 0, 0)

    avg_gain = compute_rma(gain, window)
    avg_loss = compute_rma(loss, window)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi