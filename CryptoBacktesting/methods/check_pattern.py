from collections import defaultdict
from datetime import datetime
import re
import sys



# Adjust the approach to handle parsing given the file structure
def process_trade_file(file_path):
    """
    This function is used to analyze the backtesting results.
    It checks at which time ranges of the day the trade success.
    """
    time_ranges = defaultdict(lambda: {'trades': 0, 'losses': 0})
    current_trade_time = None  # To keep track of the trade's trigger time

    with open(file_path, 'r') as file:
        for line in file:
            # Check for trade trigger line
            trigger_match = re.search(r"position triggered at (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", line)
            if trigger_match:
                current_trade_time = trigger_match.group(1)
            
            # Check for profit/loss line
            profit_match = re.search(r"Profit: ([-\d.]+)", line)
            if profit_match and current_trade_time:
                profit = float(profit_match.group(1))
                time_range = categorize_trade_time(current_trade_time)
                time_ranges[time_range]['trades'] += 1
                if profit < 0:
                    time_ranges[time_range]['losses'] += 1
                current_trade_time = None  # Reset for the next trade

    return time_ranges
# Categorize trade time
def categorize_trade_time(trade_time):
    trade_datetime = datetime.strptime(trade_time, "%Y-%m-%d %H:%M")
    if trade_datetime.hour < 3:
        return "00:00-02:59"
    elif trade_datetime.hour < 6:
        return "03:00-5:59"
    elif trade_datetime.hour < 9:
        return "6:00-8:59"
    elif trade_datetime.hour < 12:
        return "09:00-11:59"
    elif trade_datetime.hour < 15:
        return "12:00-14:59"
    elif trade_datetime.hour < 18:
        return "15:00-17:59"
    elif trade_datetime.hour < 21:
        return "18:00-20:59"
    else:
        return "21:00-23:59"



def print_losing_time_ranges(time_ranges):
    file_name = "checkingoutputlast.txt"
    file = open(file_name, "w")

    # Save the original stdout so that we can revert sys.stdout after we're done
    original_stdout = sys.stdout 

    # Redirect stdout to the file
    sys.stdout = file
    for time_range, stats in time_ranges.items():
        if stats['losses'] > 0:
            print(f"{time_range}: {stats['losses']} losses out of {stats['trades']} trades")
    sys.stdout = original_stdout

    # Close the file
    file.close()

# Example usage
file_path = "checking2.txt"
time_ranges = process_trade_file(file_path)
print_losing_time_ranges(time_ranges)