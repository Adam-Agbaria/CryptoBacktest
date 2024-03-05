from datetime import datetime, timedelta

# Trading parameters and initial settings
symbol = 'BNB/USDT'
starting_cash = 0
cash = starting_cash
max_portfolio_value = starting_cash
min_portfolio_value = starting_cash
cumulative_profit_loss = 0

time_limit = True
invalidated_lines = {}  # Store invalidated lines
inval_once = {}
TwoLPorhib = True
timeframe1d = '1d'
timeframe5m = '5m'
timeframe1m = '1m'
same_sl_all = 0.0125 #SL
same_tp_all = same_sl_all #TP 
detailed_trend = True
time_limit_release = True

start_date = datetime.now() - timedelta(days=170)
end_date = datetime.now() - timedelta(days=40)

# Initialize dictionaries for daily and weekly profits
daily_profit = {}
weekly_profit = {}

current_week = 1
weekly_cumulative_profit = 0
last_day_profit = 0

# Reset day_count to 0 at the beginning of the loop
day_count = 0



trade_triggers = {'hit_high_from_below Neutral',
                  'hit_high_from_below Bullish',
                  'hit_high_from_below Bearish',
                  'hit_low_from_above Neutral',
                  'hit_low_from_above Bullish',
                  'hit_low_from_above Bearish',
                  'hit_mid_from_above Neutral',
                  'hit_mid_from_above Bullish',
                  'hit_mid_from_above Bearish',
                  'hit_mid_from_below Neutral',
                  'hit_mid_from_below Bullish',
                  'hit_mid_from_below Bearish',
                  'hit_fibo_0_236_from_above Neutral',
                  'hit_fibo_0_236_from_above Bullish',
                  'hit_fibo_0_236_from_above Bearish',
                  'hit_fibo_0_236_from_below Neutral',
                  'hit_fibo_0_236_from_below Bullish',
                  'hit_fibo_0_236_from_below Bearish',
                  'hit_fibo_0_786_from_above Neutral',
                  'hit_fibo_0_786_from_above Bullish',
                  'hit_fibo_0_786_from_above Bearish',
                  'hit_fibo_0_786_from_below Neutral',
                  'hit_fibo_0_786_from_below Bullish',
                  'hit_fibo_0_786_from_below Bearish',
                  'hit_ema_from_below Neutral',  
                  'hit_ema_from_above Neutral',
                  'RSI-MACD-EMA BUY strategy',
                  'RSI-MACD-EMA SELL strategy'
                   }

trade_performance = {trigger: {'success': 0, 'failure': 0} for trigger in trade_triggers}
