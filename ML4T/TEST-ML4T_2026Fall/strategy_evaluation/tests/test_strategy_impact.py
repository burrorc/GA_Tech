import datetime as dt
import pandas as pd
import numpy as np

import StrategyLearner as sl
import marketsimcode as msc

symbol = "JPM"
sd = dt.datetime(2008, 1, 1)
ed = dt.datetime(2009, 12, 31)
sv = 100000

impacts = [0.0, 0.005, 0.01, 0.02, 0.05]

results = []
trades_by_impact = {}

for impact in impacts:

    learner = sl.StrategyLearner(
        impact=impact,
        commission=0.0
    )

    learner.add_evidence(symbol, sd, ed, sv)

    trades = learner.testPolicy(symbol, sd, ed, sv)

    trades_by_impact[impact] = trades.copy()

    portvals = msc.compute_portvals(
        trades,
        start_val=sv,
        commission=0.0,
        impact=impact
    )

    values = portvals.iloc[:, 0]
    holdings = trades.cumsum()
    daily_returns = values.pct_change().dropna()

    results.append({
        "Impact": impact,
        "CR": values.iloc[-1] / values.iloc[0] - 1,
        "Transactions": (trades[symbol] != 0).sum(),
        "Shares Traded": trades[symbol].abs().sum(),
        "Long Days": (holdings[symbol] == 1000).sum(),
        "Short Days": (holdings[symbol] == -1000).sum(),
        "Cash Days": (holdings[symbol] == 0).sum(),
        "Daily Volatility": daily_returns.std(),
        "Ending Value": values.iloc[-1]
    })

df = pd.DataFrame(results)

print(df.round(6).to_string(index=False))

print("\nTRADE DIFFERENCES VS ZERO IMPACT")

for impact in impacts[1:]:

    differences = (
        trades_by_impact[0.0][symbol] !=
        trades_by_impact[impact][symbol]
    ).sum()

    print(f"Impact {impact}: {differences} different days")

df.to_csv("strategy_impact_test.csv", index=False)