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

configurations = [
    # Name, Bags, Leaf, Peek, Multiplier

    ("Aggressive", 100, 5, 5, 0.25),
    ("Moderate", 100, 10, 3, 0.35),
    ("Conservative", 100, 20, 3, 0.35)
]

runs = 5
results = []


def evaluate(trades, include_costs=True):

    portvals = msc.compute_portvals(
        trades,
        start_val=sv,
        commission=commission if include_costs else 0,
        impact=impact if include_costs else 0
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

            for persist in [False, True]:

                learner.persist_position = persist

                train_trades = learner.testPolicy(
                    symbol, train_sd, train_ed, sv
                )

                start = time.perf_counter()

                val_trades = learner.testPolicy(
                    symbol, val_sd, val_ed, sv
                )

                testing_time = time.perf_counter() - start

                for include_costs in [True, False]:

                    train_metrics = evaluate(
                        train_trades, include_costs
                    )

                    val_metrics = evaluate(
                        val_trades, include_costs
                    )

                    results.append({
                        "Symbol": symbol,
                        "Candidate": name,
                        "Run": run + 1,
                        "Persistence": persist,
                        "Costs": include_costs,
                        "Train CR": train_metrics["CR"],
                        "Val CR": val_metrics["CR"],
                        "Val Sharpe": val_metrics["Sharpe"],
                        "Val Drawdown": val_metrics["Max Drawdown"],
                        "Train Trades": train_metrics["Trades"],
                        "Val Trades": val_metrics["Trades"],
                        "Training Time": training_time,
                        "Testing Time": testing_time
                    })

        pd.DataFrame(results).to_csv(
            "strategy_persistence_runs.csv",
            index=False
        )

results_df = pd.DataFrame(results)

summary = results_df.groupby(
    ["Candidate", "Symbol", "Persistence", "Costs"]
).agg(
    train_cr_mean=("Train CR", "mean"),
    val_cr_mean=("Val CR", "mean"),
    val_cr_std=("Val CR", "std"),
    val_sharpe_mean=("Val Sharpe", "mean"),
    val_drawdown_mean=("Val Drawdown", "mean"),
    val_trades_mean=("Val Trades", "mean"),
    profitable_runs=("Val CR", lambda x: (x > 0).sum()),
    inactive_runs=("Val Trades", lambda x: (x == 0).sum())
).reset_index()

overall = results_df.groupby(
    ["Candidate", "Persistence", "Costs"]
).agg(
    train_cr_mean=("Train CR", "mean"),
    val_cr_mean=("Val CR", "mean"),
    val_cr_std=("Val CR", "std"),
    val_sharpe_mean=("Val Sharpe", "mean"),
    val_drawdown_mean=("Val Drawdown", "mean"),
    val_trades_mean=("Val Trades", "mean"),
    profitable_runs=("Val CR", lambda x: (x > 0).sum()),
    inactive_runs=("Val Trades", lambda x: (x == 0).sum())
).reset_index()

summary.to_csv(
    "strategy_persistence_summary.csv",
    index=False
)

overall.to_csv(
    "strategy_persistence_overall.csv",
    index=False
)

print(overall.round(6).to_string(index=False))