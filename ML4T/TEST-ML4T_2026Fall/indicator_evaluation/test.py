import datetime as dt
import TheoreticallyOptimalStrategy as tos

trades = tos.testPolicy(
    symbol="JPM",
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 12, 31),
    sv=100000
)

print(trades.head(10))
print(trades.tail(10))

print("Unique trade values:", trades.iloc[:, 0].unique())

holdings = trades.iloc[:, 0].cumsum()

print("Unique holdings:", holdings.unique())
print("Maximum position:", holdings.max())
print("Minimum position:", holdings.min())