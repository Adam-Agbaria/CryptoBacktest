import os
import pandas as pd
from fetch_data import fetch_data_loop


def save_data_to_file(data, filename):
    """Save the data to a CSV file."""
    data.to_csv(filename, index=True)


    
def load_data_from_file(filename, start_date, end_date):
    """
    Load data from a CSV file, parse dates, and filter it for a specific date range.

    :param filename: Path to the file to load
    :param start_date: Start date as a string in 'YYYY-MM-DD' format
    :param end_date: End date as a string in 'YYYY-MM-DD' format
    :return: Filtered DataFrame
    """
    df = pd.read_csv(filename, index_col='timestamp', parse_dates=True)
    filtered_df = df.loc[start_date:end_date]
    return filtered_df

def fetch_and_save_data(symbol, timeframe, start_date, end_date, filename):
    """Fetch data from Binance and save it to a file, or load from the file if it already exists."""
    if os.path.exists(filename):
        print(f"Loading data from {filename}")
        return load_data_from_file(filename, start_date, end_date)
    else:
        print(f"Fetching data from Binance for {symbol} from {start_date} to {end_date}")
        data = fetch_data_loop(symbol, timeframe, start_date, end_date)
        save_data_to_file(data, filename)
        return data

import pandas as pd

def add_indicators(data):
    # Calculate MACD
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()

    # Calculate RSI
    delta = data['close'].diff()
    gain = (delta.clip(lower=0)).rolling(window=14).mean()
    loss = (-delta.clip(upper=0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Calculate EMA50, EMA100, and EMA200
    ema50 = data['close'].ewm(span=50, adjust=False).mean()
    ema100 = data['close'].ewm(span=100, adjust=False).mean()
    ema200 = data['close'].ewm(span=200, adjust=False).mean()

    # Add the indicators to the DataFrame
    data['macd'] = macd
    data['signal'] = signal
    data['rsi'] = rsi
    data['ema50'] = ema50
    data['ema100'] = ema100
    data['ema200'] = ema200

    return data

