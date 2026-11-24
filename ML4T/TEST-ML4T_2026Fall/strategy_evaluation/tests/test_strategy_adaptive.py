import datetime as dt
import numpy as np
import pandas as pd
import time


import StrategyLearner as sl
import marketsimcode as msc

import indicators as ind


symbols = ["JPM", "MSFT", "IBM", "GE", "XOM"]
sv = 100000
impact = 0.005
commission = 9.95

train_sd = dt.datetime(2008, 1, 1)
train_ed = dt.datetime(2008, 12, 31)

val_sd = dt.datetime(2009, 1, 1)
val_ed = dt.datetime(2009, 12, 31)

configurations = []

for leaf in [5, 10, 20]:
    for peek in [3, 5]:
        for multiplier in [0.15, 0.25, 0.35]:

            name = f"Adaptive_L{leaf}_P{peek}_M{multiplier}"

            configurations.append(
                (name, 100, leaf, peek, multiplier)
            )

runs = 5
results = []


def evaluate(trades):

    portvals = msc.compute_portvals(
        trades,
        start_val=sv,
        commission=commission,
        impact=impact
    )

    values = portvals.iloc[:, 0]

    daily_returns = values.pct_change().dropna()

    cr = values.iloc[-1] / values.iloc[0] - 1

    sharpe = (
        np.sqrt(252) *
        daily_returns.mean() /
        daily_returns.std()
        if daily_returns.std() > 0 else np.nan
    )

    drawdown = values / values.cummax() - 1

    return {
        "CR": cr,
        "Sharpe": sharpe,
        "Max Drawdown": drawdown.min(),
        "Trades": (trades.iloc[:, 0] != 0).sum(),
        "Ending Value": values.iloc[-1]
    }

def get_benchmark(symbol, sd, ed):

    prices, features = ind.get_features(symbol, sd, ed)

    trades = pd.DataFrame(
        0, index=prices.index, columns=[symbol]
    )

    trades.iloc[0, 0] = 1000

    return trades


for symbol in symbols:

    benchmark_trades = get_benchmark(
        symbol, val_sd, val_ed
    )

    benchmark_metrics = evaluate(benchmark_trades)

    for name, bags, leaf, peek, multiplier in configurations:

        print(
            f"{symbol}: {name}",
            flush=True
        )

        for run in range(runs):

            learner = sl.StrategyLearner(
                impact=impact,
                commission=commission
            )

            learner.bags = bags
            learner.leaf_size = leaf
            learner.peek = peek
            learner.adaptive = True
            learner.vol_multiplier = multiplier

            start = time.perf_counter()

            learner.add_evidence(
                symbol, train_sd, train_ed, sv
            )

            training_time = time.perf_counter() - start

            train_trades = learner.testPolicy(
                symbol, train_sd, train_ed, sv
            )

            start = time.perf_counter()

            val_trades = learner.testPolicy(
                symbol, val_sd, val_ed, sv
            )

            testing_time = time.perf_counter() - start

            train_metrics = evaluate(train_trades)
            val_metrics = evaluate(val_trades)

            results.append({
                "Symbol": symbol,
                "Candidate": name,
                "Bags": bags,
                "Leaf": leaf,
                "Peek": peek,
                "Multiplier": multiplier,
                "Run": run + 1,
                "Train CR": train_metrics["CR"],
                "Val CR": val_metrics["CR"],
                "Benchmark CR": benchmark_metrics["CR"],
                "Excess CR": (
                    val_metrics["CR"] -
                    benchmark_metrics["CR"]
                ),
                "Val Sharpe": val_metrics["Sharpe"],
                "Val Drawdown": val_metrics["Max Drawdown"],
                "Train Trades": train_metrics["Trades"],
                "Val Trades": val_metrics["Trades"],
                "Training Time": training_time,
                "Testing Time": testing_time
            })

        pd.DataFrame(results).to_csv(
            "strategy_adaptive_runs.csv",
            index=False
        )

results_df = pd.DataFrame(results)

summary = results_df.groupby(
    ["Candidate", "Symbol"]
).agg(
    train_cr_mean=("Train CR", "mean"),
    val_cr_mean=("Val CR", "mean"),
    benchmark_cr=("Benchmark CR", "mean"),
    excess_cr_mean=("Excess CR", "mean"),
    val_cr_std=("Val CR", "std"),
    val_cr_min=("Val CR", "min"),
    val_sharpe_mean=("Val Sharpe", "mean"),
    val_drawdown_mean=("Val Drawdown", "mean"),
    val_trades_mean=("Val Trades", "mean"),
    profitable_runs=("Val CR", lambda x: (x > 0).sum()),
    benchmark_wins=("Excess CR", lambda x: (x > 0).sum()),
    inactive_runs=("Val Trades", lambda x: (x == 0).sum())
).reset_index()

summary.to_csv(
    "strategy_adaptive_summary.csv",
    index=False
)

overall = results_df.groupby("Candidate").agg(
    val_cr_mean=("Val CR", "mean"),
    val_cr_median=("Val CR", "median"),
    excess_cr_mean=("Excess CR", "mean"),
    val_sharpe_mean=("Val Sharpe", "mean"),
    val_drawdown_mean=("Val Drawdown", "mean"),
    val_trades_mean=("Val Trades", "mean"),
    profitable_runs=("Val CR", lambda x: (x > 0).sum()),
    benchmark_wins=("Excess CR", lambda x: (x > 0).sum()),
    inactive_runs=("Val Trades", lambda x: (x == 0).sum()),
    max_training_time=("Training Time", "max"),
    max_testing_time=("Testing Time", "max")
).reset_index()

overall = overall.sort_values(
    by="excess_cr_mean", ascending=False
)

overall.to_csv(
    "strategy_adaptive_overall.csv",
    index=False
)

print("\nOVERALL RESULTS")
print(overall.to_string(index=False))