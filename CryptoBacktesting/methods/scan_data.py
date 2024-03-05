import pandas as pd
import sys
from trend_locator import determine_trend, calculate_previous_levels,extract_lines_from_day_row
from potential_triggers import check_potential_trigger, terminate_trade
from collections import defaultdict
from prints import printProfits, print_trade_performance
from data_download import load_data_from_file
from utils import get_last_weeks_rsi, get_yesterdays_rsi, get_previous_1m_candle_rsi
sys.path.append('..')
from constants.parameters import  start_date, end_date, invalidated_lines, cash, same_tp_all, same_sl_all, time_limit_release
from constants.parameters import trade_performance
sys.path.append('.')


file_name = "output.txt"
file = open(file_name, "w")

# Save the original stdout so that we can revert sys.stdout after we're done
original_stdout = sys.stdout 

# Redirect stdout to the file
sys.stdout = file



daily_data = load_data_from_file("daily_data.csv", start_date, end_date)
intraday_data = load_data_from_file("intraday_data1m.csv", start_date, end_date)
weekly_data = load_data_from_file("weekly_data.csv", start_date, end_date)

daily_percent_gains = defaultdict(float)


# Function to process each day's 5-minute data
def process_daily_intraday_data(daily_data, intraday_data, cash, time_limit_release, trade_triggers):
    # Apply determine_trend and calculate_previous_levels functions
    daily_data = calculate_previous_levels(daily_data)
    intraday_data['prev_close'] = intraday_data['close'].shift()
    position = None
    trend = 'Neutral'
    percent_gain = 0
    trades_won = 0
    trades_lost = 0
    min_pc_gain = 0
    max_pc_gain = 0


    for index, day_row in daily_data.iterrows():
        day = index.date()  # Extract the date
        print(f"Processing data for {day}")
        
        # Filter intraday data for the current day
        day_intraday_data = intraday_data[intraday_data.index.date == day]
        percent_gain_daily = 0

        lines = extract_lines_from_day_row(day_row)
        lines['weekly_rsi'] = get_last_weeks_rsi(weekly_data, day)
        lines['daily_rsi'] = get_yesterdays_rsi(daily_data, day)


        trend = 'Neutral'
        trend = determine_trend(lines)
        print(f"High: {round(lines['high'],3)} 0.786: {round(lines['c0_786'],3)} Mid:{round(lines['mid'],3)} 0.236: {round(lines['c0_236'],3)} Low: {round(lines['low'],3)} PrevTrend: {trend}")
        
        for intraday_index, intraday_row in day_intraday_data.iterrows():
            current_time = intraday_index.time()
            lines['prev_close'] = intraday_row['prev_close']
            lines['previous_1m_rsi'] = get_previous_1m_candle_rsi(intraday_data, intraday_index)

            
           
            if position == None: ##If not in position check for potenital trade triggers 
                trade = check_potential_trigger(intraday_row, lines, invalidated_lines, day, trend)
                if trade != None:
                    position = trade['position']
                    
                
            if position != None: ##If in position check if TP or SL prices were hit and terminate in case they do
                points_gained, status, trade = terminate_trade(trade, intraday_row, intraday_index, lines, day, invalidated_lines)
                if status == 'Terminated':
                    position = None
                    trigger = trade['trade_trigger']
                    if trigger not in trade_performance:
                        # If not, initialize it with a dictionary that has a 'success' key set to 0
                        trade_performance[trigger] = {'success': 0, 'failure': 0}
                    if( points_gained > 0):
                        percent_gain += (same_tp_all * 100)
                        percent_gain_daily+= (same_tp_all * 100)
                        trades_won += 1
                        trade_performance[trigger]['success'] += 1
                    elif(points_gained < 0):
                        percent_gain -= (same_sl_all * 100)
                        percent_gain_daily-= (same_sl_all * 100)
                        trades_lost += 1
                        trade_performance[trigger]['failure'] += 1

                    max_pc_gain = max(percent_gain, max_pc_gain)
                    min_pc_gain = min(percent_gain, min_pc_gain)
            daily_percent_gains[index.date()] = percent_gain_daily


    total_trades = trades_won + trades_lost
    printProfits(daily_percent_gains)
    print_trade_performance(trade_performance)
    print(f"\nTotal amount of Trades: {total_trades} Trades won: {trades_won} Trades lost: {trades_lost}")
    print(f"Trades won percentage: {(trades_won/total_trades) * 100}%")
    print(f"Maximum percent gain: {max_pc_gain}")
    print(f"Maximum percent loss: {min_pc_gain}")

    return percent_gain

percent_gain = process_daily_intraday_data(daily_data, intraday_data, cash, time_limit_release, trade_performance)
print(f"Total percent gain: {percent_gain}")

sys.stdout = original_stdout

# Close the file
file.close()