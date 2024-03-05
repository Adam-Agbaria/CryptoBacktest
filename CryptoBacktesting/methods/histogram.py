import pandas as pd
import matplotlib.pyplot as plt
import re

def parse_trade_data(file_path):
    # Regex patterns
    date_line_pattern = re.compile(r"Processing data for (\d{4}-\d{2}-\d{2})")
    trade_line_pattern = re.compile(r"(\d{2}:\d{2}) .* Profit: ([-\d.]+)")
    week_line_pattern = re.compile(r"Week \d+ of \d+: \d+\.\d+")
    best_line_pattern = re.compile(r"Best")


    trades = []
    current_date = None

    with open(file_path, 'r') as f:
        for line in f:
            best_match = best_line_pattern.match(line)
            if best_match:
                print(line)
                break
            date_match = date_line_pattern.match(line)
            if date_match:
                # Extract the date for subsequent trades
                current_date = date_match.group(1)
                continue  # Skip to next line

            week_match = week_line_pattern.match(line)

            trade_match = trade_line_pattern.search(line)
            if trade_match and current_date:
                # Extracting time and profit
                time_str = trade_match.group(1)
                profit = float(trade_match.group(2))
                profit/=2
                datetime_str = f"{current_date} {time_str}"
                try:
                    datetime_obj = pd.to_datetime(datetime_str)
                    trades.append((datetime_obj, profit))
                except ValueError as e:
                    print(f"Error parsing datetime: {datetime_str}, error: {e}")

    # Create DataFrame from trades
    if trades:
        df = pd.DataFrame(trades, columns=['Datetime', 'Profit'])
        df.set_index('Datetime', inplace=True)
        return df
    else:
        print("No trade data found.")
        return pd.DataFrame()

def plot_cumulative_profits(df):
    if not df.empty:
        df['Cumulative Profit'] = df['Profit'].cumsum()
        df['Cumulative Profit'].plot(figsize=(14, 7))
        plt.title('Cumulative Profits Over Time')
        plt.xlabel('Datetime')
        plt.ylabel('Cumulative Profit')
        plt.grid(True)
        plt.show()
    else:
        print("Empty DataFrame, no data to plot.")


# Replace with your actual file path
# file_path = 'Strat-Results/x1point2/0point5pc/0point5pctpx1point2.txt'
file_path = 'Strat-Results/NeutralSecond/test.txt'


# Read trade data
df_trades = parse_trade_data(file_path)

if not df_trades.empty:
    plot_cumulative_profits(df_trades)
else:
    print('No trade data found.')



