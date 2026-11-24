import datetime as dt
import pandas as pd
import indicators as ind

from util import get_data

symbol = "JPM"

sd = dt.datetime(2008, 1, 1)
ed = dt.datetime(2009, 12, 31)

prefill_sd = sd - dt.timedelta(days=90)
dates = pd.date_range(prefill_sd, ed)

prices = get_data([symbol], dates)[symbol]

high = get_data(
    [symbol], dates, colname="High"
)[symbol]

low = get_data(
    [symbol], dates, colname="Low"
)[symbol]

close = get_data(
    [symbol], dates, colname="Close"
)[symbol]

features = pd.DataFrame(index=prices.index)

features["BB"] = ind.bollinger_b(prices)
features["MACD"] = ind.macd_histo(prices)
features["MOM"] = ind.momentum(prices)
features["SMA"] = ind.price_over_sma(prices)
features["CCI"] = ind.cci(high, low, close)

features = features.shift(1)
features = features.loc[sd:ed].dropna()

correlation = features.corr()

print("\nINDICATOR CORRELATION")
print(correlation.round(4))

print("\nOBSERVATIONS")
print(len(features))