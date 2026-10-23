import datetime as dt
import pandas as pd

from util import get_data
from indicators import price_over_sma, bollinger_b, momentum, macd_histo, cci
import matplotlib.pyplot as plt


symbol = "JPM"
sd = dt.datetime(2008, 1, 1)
ed = dt.datetime(2009, 12, 31)

backfill_date = sd - dt.timedelta(days=60)

dates = pd.date_range(backfill_date, ed)
prices = get_data([symbol], dates)[symbol]

# SMA RATIO

# sma = prices.rolling(window=20).mean()
# sma_ratio = price_over_sma(prices, window=20)

# results = pd.DataFrame({
#     "Price": prices,
#     "SMA_20": sma,
#     "Price_SMA": sma_ratio
# })

# results = results.loc[sd:ed]

# print(results.head(10))
# print("Missing values:", results["Price_SMA"].isna().sum())

# normalized_price = results["Price"] / results["Price"].iloc[0]
# normalized_sma = results["SMA_20"] / results["Price"].iloc[0]

# fig, (ax1, ax2) = plt.subplots(
#     2, 1,
#     figsize=(12, 8),
#     sharex=True
# )

# ax1.plot(results.index, normalized_price, label="JPM Price")
# ax1.plot(results.index, normalized_sma, label="20-Day SMA")
# ax1.set_title("JPM: 20-Day SMA and Price/SMA Ratio")
# ax1.set_ylabel("Normalized Price")
# ax1.legend()
# ax1.grid(True)

# ax2.plot(results.index, results["Price_SMA"], color="green", label="Price/SMA Ratio")
# ax2.axhline(1.0, color="gray", linestyle="--", label="Ratio = 1.0")
# ax2.set_xlabel("Date")
# ax2.set_ylabel("Price/SMA Ratio")
# ax2.legend()
# ax2.grid(True)

# plt.tight_layout()
# plt.savefig("sma_indicator.png")
# plt.close()

# BOLLINGER %B

# percent_b = bollinger_b(prices)

# results = pd.DataFrame({
#     "Price": prices,
#     "BB_Percent": percent_b
# })

# results = results.loc[sd:ed]

# print(results.head(10))
# print("Missing values:", results["BB_Percent"].isna().sum())

# sma = prices.rolling(window=20).mean()
# std = prices.rolling(window=20).std()

# upper_band = sma + 2 * std
# lower_band = sma - 2 * std

# bb_results = pd.DataFrame({
#     "Price": prices,
#     "SMA": sma,
#     "Upper": upper_band,
#     "Lower": lower_band,
#     "Percent_B": percent_b
# }).loc[sd:ed]

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# ax1.plot(bb_results.index, bb_results["Price"], label="JPM Price")
# ax1.fill_between(
#     bb_results.index,
#     bb_results["Lower"],
#     bb_results["Upper"],
#     alpha=0.2,
#     label="Bollinger Band Range"
# )

# ax1.set_title("JPM: Bollinger Bands and %B (20-Day, 2 Std Dev)")
# ax1.set_ylabel("Price ($)")
# ax1.legend()
# ax1.grid(True)

# ax2.plot(bb_results.index, bb_results["Percent_B"], color="green", label="Bollinger %B")
# ax2.axhline(1.0, color="red", linestyle="--", label="Upper Band (1.0)")
# ax2.axhline(0.0, color="blue", linestyle="--", label="Lower Band (0.0)")
# ax2.axhline(0.5, color="gray", linestyle=":", label="Middle Band (0.5)")

# ax2.set_xlabel("Date")
# ax2.set_ylabel("Bollinger %B")
# ax2.legend()
# ax2.grid(True)

# plt.tight_layout()
# plt.savefig("bollinger_indicator.png")
# plt.close()


# MOMENTUM
# momentum_values = momentum(prices, window=10)

# momentum_results = pd.DataFrame({
#     "Price": prices,
#     "Price_10_Days_Ago": prices.shift(10),
#     "Momentum": momentum_values
# }).loc[sd:ed]

# print(momentum_results.head(10))
# print("Missing values:", momentum_results["Momentum"].isna().sum())

# normalized_price = momentum_results["Price"] / momentum_results["Price"].iloc[0]

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# ax1.plot(
#     momentum_results.index,
#     normalized_price,
#     label="JPM Price"
# )
# ax1.set_title("JPM: 10-Day Momentum")
# ax1.set_ylabel("Normalized Price")
# ax1.legend()
# ax1.grid(True)

# ax2.bar(
#     momentum_results.index,
#     momentum_results["Momentum"],
#     color=[
#         "green" if value >= 0 else "red"
#         for value in momentum_results["Momentum"]
#     ],
#     width=2
# )

# ax2.axhline(0, color="gray", linestyle="--")

# plt.tight_layout()
# plt.savefig("momentum_indicator.png")
# plt.close()


# MACD HISTO
# macd_values = macd_histo(prices)

# macd_results = pd.DataFrame({
#     "Price": prices,
#     "MACD_Histogram": macd_values
# }).loc[sd:ed]

# fast_ema = prices.ewm(span=12, adjust=False).mean()
# slow_ema = prices.ewm(span=26, adjust=False).mean()

# macd_line = fast_ema - slow_ema
# signal_line = macd_line.ewm(span=9, adjust=False).mean()

# macd_chart = pd.DataFrame({
#     "MACD": macd_line,
#     "Signal": signal_line,
#     "Histogram": macd_values
# }).loc[sd:ed]

# fig, (ax1, ax2) = plt.subplots(
#     2, 1, figsize=(12, 8), sharex=True
# )

# ax1.plot(macd_chart.index, macd_chart["MACD"], label="MACD")
# ax1.plot(macd_chart.index, macd_chart["Signal"], label="Signal Line")
# ax1.axhline(0, color="gray", linestyle="--")
# ax1.set_title("JPM: MACD Histogram (12, 26, 9)")
# ax1.set_ylabel("MACD")
# ax1.legend()
# ax1.grid(True)

# ax2.bar(
#     macd_chart.index,
#     macd_chart["Histogram"],
#     color=[
#         "green" if value >= 0 else "red"
#         for value in macd_chart["Histogram"]
#     ],
#     width=2
# )

# ax2.axhline(0, color="gray", linestyle="--")
# ax2.set_xlabel("Date")
# ax2.set_ylabel("MACD Histogram")
# ax2.grid(True)

# plt.tight_layout()
# plt.savefig("macd_indicator.png")
# plt.close()

# CCI

high = get_data([symbol], dates, colname="High")[symbol]
low = get_data([symbol], dates, colname="Low")[symbol]
close = get_data([symbol], dates, colname="Close")[symbol]

cci_values = cci(high, low, close, window=20)

cci_results = pd.DataFrame({
    "Close": close,
    "CCI": cci_values
}).loc[sd:ed]

print(cci_results.head(10))
print("Missing values:", cci_results["CCI"].isna().sum())
print("Minimum:", cci_results["CCI"].min())
print("Maximum:", cci_results["CCI"].max())

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

ax1.plot(cci_results.index, cci_results["Close"], label="JPM Closing Price")
ax1.set_title("JPM: Commodity Channel Index (20-Day)")
ax1.set_ylabel("Closing Price ($)")
ax1.legend()
ax1.grid(True)

ax2.plot(cci_results.index, cci_results["CCI"], color="purple", label="CCI")
ax2.axhline(100, color="green", linestyle="--", label="+100")
ax2.axhline(-100, color="red", linestyle="--", label="-100")
ax2.axhline(0, color="gray", linestyle=":", label="Zero")

ax2.set_xlabel("Date")
ax2.set_ylabel("CCI")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("cci_indicator.png")
plt.close()
