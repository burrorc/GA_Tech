
import datetime as dt

import pandas as pd
from util import get_data
from marketsimcode import compute_portvals

# Load a few trading days.
dates = pd.date_range(
    dt.datetime(2008, 1, 2),
    dt.datetime(2008, 1, 10)
)

prices = get_data(["JPM"], dates)[["JPM"]]

# Create one trade: buy 1,000 shares on the first day.
trades = pd.DataFrame(0, index=prices.index, columns=["JPM"])
trades.iloc[0, 0] = 1000   # Buy 1000 on Jan 2
trades.iloc[2, 0] = -2000  # Sell 2000 on Jan 4

portvals = compute_portvals(
   trades_df=trades,
    start_val=100000,
    commission=9.95,
    impact=0.005
)

print("Prices:")
print(prices)

print("\nTrades:")
print(trades)

print("\nPortfolio values:")
print(portvals)
