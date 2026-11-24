import datetime as dt
import pandas as pd

import StrategyLearner as sl
import indicators as ind
import numpy as np

symbols = ["JPM", "MSFT", "IBM", "GE", "XOM"]

sd = dt.datetime(2008, 1, 1)
ed = dt.datetime(2008, 12, 31)

configurations = [
    ("SL-V2", 5, 0.01),
    ("Candidate B", 3, 0.03)
]

results = []

for name, peek, threshold in configurations:

    for symbol in symbols:

        learner = sl.StrategyLearner(
            impact=0.005,
            commission=9.95
        )

        learner.peek = peek
        learner.threshold = threshold

        prices, features = ind.get_features(
            symbol, sd, ed
        )

        labels = learner.get_labels(prices).dropna()

        counts = labels.value_counts(normalize=True)

        results.append({
            "Candidate": name,
            "Symbol": symbol,
            "Short %": counts.get(-1, 0) * 100,
            "Cash %": counts.get(0, 0) * 100,
            "Long %": counts.get(1, 0) * 100,
            "Daily Volatility %": (
                prices.pct_change().std() * 100
            )
        })

df = pd.DataFrame(results)

print(df.round(2).to_string(index=False))

df.to_csv("strategy_label_distribution.csv", index=False)

adaptive_results = []

multipliers = [0.25, 0.5, 0.75, 1.0]
peek = 3

for multiplier in multipliers:

    for symbol in symbols:

        prices, features = ind.get_features(
            symbol, sd, ed
        )

        volatility = (
            prices.pct_change()
            .rolling(window=20)
            .std()
            .shift(1)
        )

        future_returns = prices.shift(-peek) / prices - 1

        commission_fee = 2 * 9.95 / (1000 * prices)

        threshold = (
            multiplier * volatility * np.sqrt(peek)
            + 2 * 0.005
            + commission_fee
        )

        labels = pd.Series(0, index=prices.index)

        labels.loc[future_returns > threshold] = 1
        labels.loc[future_returns < -threshold] = -1

        valid = (
            future_returns.notna()
            & threshold.notna()
        )

        labels = labels.loc[valid]

        counts = labels.value_counts(normalize=True)

        adaptive_results.append({
            "Multiplier": multiplier,
            "Symbol": symbol,
            "Short %": counts.get(-1, 0) * 100,
            "Cash %": counts.get(0, 0) * 100,
            "Long %": counts.get(1, 0) * 100,
            "Avg Threshold %": threshold.loc[valid].mean() * 100
        })

adaptive_df = pd.DataFrame(adaptive_results)

print("\nADAPTIVE THRESHOLD RESULTS")
print(adaptive_df.round(2).to_string(index=False))

adaptive_df.to_csv(
    "strategy_adaptive_labels.csv",
    index=False
)