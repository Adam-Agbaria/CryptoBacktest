import ccxt
import pandas as pd
import time as tm

# Initialize the Binance exchange
exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'  # or 'delivery' for delivery futures
    }
})

# Function to fetch historical data
def fetch_data(symbol, timeframe, since, limit=500):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# Convert timeframe string to milliseconds
def timeframe_to_milliseconds(timeframe):
    amount = int(timeframe[:-1])
    unit = timeframe[-1]
    if unit == 'm':
        return amount * 60 * 1000
    elif unit == 'h':
        return amount * 60 * 60 * 1000
    elif unit == 'd':
        return amount * 24 * 60 * 60 * 1000
    elif unit == 'w':
        return amount * 7 * 24 * 60 * 60 * 1000
    else:
        raise ValueError("Unsupported timeframe")


# Function to fetch historical data within a date range
def fetch_data_loop(symbol, timeframe, start_date, end_date):
    since = exchange.parse8601(str(start_date))
    print("Start date (since):", start_date)

    all_data = pd.DataFrame()

    while True:
        data = fetch_data(symbol, timeframe, since)
        if data.empty:
            break

        all_data = pd.concat([all_data, data])
        last_timestamp = data.index[-1]  # Get the last timestamp from the index
        since = int(last_timestamp.timestamp() * 1000) + timeframe_to_milliseconds(timeframe)

        # Break the loop if 'since' exceeds the 'end_date'
        if since > exchange.parse8601(str(end_date)):
            break

        tm.sleep(exchange.rateLimit / 1000)  # Respect the rateLimit

    return all_data
