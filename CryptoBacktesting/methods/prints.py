from utils import get_week_number

from collections import defaultdict

def printProfits(daily_gains):
    print("\nProfits made in percentage:")
    
    # Initialize tracking variables
    best_day = worst_day = best_week = worst_week = best_month = worst_month = None
    best_day_gain = best_week_gain = best_month_gain = float('-inf')
    worst_day_gain = worst_week_gain = worst_month_gain = float('inf')
    positive_months = 0
    negative_months = 0

    # Calculate weekly and monthly gains
    weekly_gains = defaultdict(float)
    monthly_gains = defaultdict(float)

    for date, gain in daily_gains.items():
        week_year = get_week_number(date)
        month_year = (date.year, date.month)
        
        weekly_gains[week_year] += gain
        monthly_gains[month_year] += gain

        # Update best and worst day
        if gain > best_day_gain:
            best_day_gain = gain
            best_day = date
        if gain < worst_day_gain:
            worst_day_gain = gain
            worst_day = date

    # Update best and worst week and month
    for period, gain in weekly_gains.items():
        if gain > best_week_gain:
            best_week_gain = gain
            best_week = period
        if gain < worst_week_gain:
            worst_week_gain = gain
            worst_week = period

    for period, gain in monthly_gains.items():
        if gain > best_month_gain:
            best_month_gain = gain
            best_month = period
        if gain < worst_month_gain:
            worst_month_gain = gain
            worst_month = period
        if gain > 0:
            positive_months += 1
        if gain < 0:
            negative_months += 1
    # Print weekly gains
    for week_year, gain in weekly_gains.items():
        year, week_number = week_year
        print(f"Week {week_number} of {year}: {gain:.1f}")
        # Print daily gains within the week
        for date, daily_gain in daily_gains.items():
            if get_week_number(date) == week_year:
                print(f"  {date}: {daily_gain:.1f}")

    # Print best and worst periods
    print(f"\nBest Day: {best_day} with a gain of {best_day_gain:.1f}%")
    print(f"Worst Day: {worst_day} with a loss of {worst_day_gain:.1f}%")
    print(f"Best Week: Week {best_week[1]} of {best_week[0]} with a gain of {best_week_gain:.1f}%")
    print(f"Worst Week: Week {worst_week[1]} of {worst_week[0]} with a loss of {worst_week_gain:.1f}%")
    print(f"Best Month: {best_month[0]}-{best_month[1]} with a gain of {best_month_gain:.1f}%")
    print(f"Worst Month: {worst_month[0]}-{worst_month[1]} with a loss of {worst_month_gain:.1f}%")
    print(f"Amount of positive monthly gains: {positive_months} Amount of negative monthly gains: {negative_months}")


def print_trade_performance(trade_performance):
    print("\nTrade Performance:")

    # Calculate success percentage for each trigger and sort by this percentage
    sorted_performance = sorted(trade_performance.items(), key=lambda item: (item[1]['success'] / (item[1]['success'] + item[1]['failure'])) if (item[1]['success'] + item[1]['failure']) > 0 else 0, reverse=True)

    for trigger, performance in sorted_performance:
        total_trades = performance['success'] + performance['failure']
        # Only print details if there are trades for this trigger
        if total_trades > 0:
            success_percentage = (performance['success'] / total_trades) * 100
            print(f"Trigger: {trigger}")
            print(f"  Successful Trades: {performance['success']}")
            print(f"  Failed Trades: {performance['failure']}")
            print(f"  Total Trades: {total_trades}")
            print(f"  Success Percentage: {success_percentage:.1f}%\n")

# def print_trade_performance(trade_performance):
#     print("\nTrade Performance:")
#     for trigger, performance in trade_performance.items():
#         total_trades = performance['success'] + performance['failure']

#         # Only print details if there are trades for this trigger
#         if total_trades > 0:
#             success_percentage = (performance['success'] / total_trades) * 100

#             print(f"Trigger: {trigger}")
#             print(f"  Successful Trades: {performance['success']}")
#             print(f"  Failed Trades: {performance['failure']}")
#             print(f"  Total Trades: {total_trades}")
#             print(f"  Success Percentage: {success_percentage:.1f}%\n")
