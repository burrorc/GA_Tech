import datetime as dt
import numpy as np
import pandas as pd
import time

import StrategyLearner as sl
import marketsimcode as msc

symbol = "JPM"
sd = dt.datetime(2008, 1, 1)
ed = dt.datetime(2009, 12, 31)
sv = 100000

learner = sl.StrategyLearner(
    verbose=False,
    impact=0.005,
    commission=9.95
)

# Train learner
start = time.perf_counter()

learner.add_evidence(symbol, sd, ed, sv)

training_time = time.perf_counter() - start

# Test learner
start = time.perf_counter()

trades = learner.testPolicy(symbol, sd, ed, sv)

testing_time = time.perf_counter() - start

# Verify trading behavior
holdings = trades.cumsum()

print("TRADES")
print(trades.head(20))

print("\nTRADE COUNTS")
print(trades[symbol].value_counts())

print("\nHOLDING COUNTS")
print(holdings[symbol].value_counts())

print("\nTOTAL TRANSACTIONS")
print((trades[symbol] != 0).sum())

print("\nVALID TRADES")
print(trades[symbol].isin(
    [-2000, -1000, 0, 1000, 2000]
).all())

print("\nVALID HOLDINGS")
print(holdings[symbol].isin(
    [-1000, 0, 1000]
).all())

print("\nCONSISTENT PREDICTIONS")
print(trades.equals(
    learner.testPolicy(symbol, sd, ed, sv)
))

# Evaluate portfolio performance
portvals = msc.compute_portvals(
    trades,
    start_val=sv,
    commission=learner.commission,
    impact=learner.impact
)

values = portvals.iloc[:, 0]
cr = values.iloc[-1] / values.iloc[0] - 1

print("\nPERFORMANCE")
print(f"Cumulative Return: {cr:.6f}")
print(f"Ending Value: ${values.iloc[-1]:,.2f}")

print("\nEXECUTION TIME")
print(f"Training: {training_time:.6f} seconds")
print(f"Testing:  {testing_time:.6f} seconds")