import pandas as pd
import matplotlib.pyplot as plt
import re

def parse_trade_data(file_path):
    # Regex pattern for date and profit
    trade_line_pattern = re.compile(r"\s*(\d{4}-\d{2}-\d{2}): ([-\d.]+)")

    trades = []

    with open(file_path, 'r') as f:
        for line in f:
            trade_match = trade_line_pattern.match(line)
            if trade_match:
                # Extracting date and profit
                date_str = trade_match.group(1)
                profit = float(trade_match.group(2))
                trades.append((date_str, profit))

    # Create DataFrame from trades
    if trades:
        df = pd.DataFrame(trades, columns=['Date', 'Daily Profit'])
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        return df
    else:
        print("No trade data found.")
        return pd.DataFrame()

def plot_cumulative_profits(df):
    if not df.empty:
        df['Cumulative Profit'] = df['Daily Profit'].cumsum()
        df['Cumulative Profit'].plot(figsize=(14, 7))
        plt.title('Cumulative Profits Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Profit')
        plt.grid(True)
        plt.show()
    else:
        print("Empty DataFrame, no data to plot.")

# Replace with your actual file path
# file_path = 'Strat-Results/NeutralSecond/test.txt'
file_path = 'Strat-Results/oldstratmodern/1pc4y-60-40x2.txt'
file_path = 'Strat-Results/strat1/Fix/1pc60-40-ema.txt'
file_path = 'ULTIMATE-DETAILED1.25pc.txt'
file_path = 'ALL/AllLines/ULTIMATE-DETAILED1.25pc.txt'
file_path = 'last.txt'
file_path = 'Strat-Results/ALL/AllLines/NormUlt.txt'










# Read trade data
df_trades = parse_trade_data(file_path)

if not df_trades.empty:
    plot_cumulative_profits(df_trades)
else:
    print('No trade data found.')
