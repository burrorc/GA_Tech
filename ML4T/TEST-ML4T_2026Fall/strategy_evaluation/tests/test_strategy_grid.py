import datetime as dt
import numpy as np
import pandas as pd
import time

from itertools import product

import StrategyLearner as sl
import marketsimcode as msc


symbol = "JPM"
sv = 100000
impact = 0.005
commission = 9.95

train_sd = dt.datetime(2008, 1, 1)
train_ed = dt.datetime(2008, 12, 31)

val_sd = dt.datetime(2009, 1, 1)
val_ed = dt.datetime(2009, 12, 31)

bags_range = [50, 100, 200]
leaf_range = [20, 30, 40]
peek_range = [1, 2, 3, 4]
threshold_range = [0.02, 0.03, 0.04, 0.05]

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
        "Trades": (trades[symbol] != 0).sum(),
        "Ending Value": values.iloc[-1]
    }

configurations = list(product(
    bags_range,
    leaf_range,
    peek_range,
    threshold_range
))

for i, (bags, leaf, peek, threshold) in enumerate(
    configurations, start=1
):

    print(
        f"Configuration {i}/{len(configurations)}: "
        f"bags={bags}, leaf={leaf}, "
        f"peek={peek}, threshold={threshold}",
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
        learner.threshold = threshold

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
            "Bags": bags,
            "Leaf": leaf,
            "Peek": peek,
            "Threshold": threshold,
            "Run": run + 1,
            "Train CR": train_metrics["CR"],
            "Val CR": val_metrics["CR"],
            "Val Sharpe": val_metrics["Sharpe"],
            "Val Drawdown": val_metrics["Max Drawdown"],
            "Train Trades": train_metrics["Trades"],
            "Val Trades": val_metrics["Trades"],
            "Val Ending Value": val_metrics["Ending Value"],
            "Training Time": training_time,
            "Testing Time": testing_time
        })

    # Save progress after every configuration
    pd.DataFrame(results).to_csv(
        "strategy_grid_v2_runs.csv", index=False
    )


results_df = pd.DataFrame(results)

summary = results_df.groupby(
    ["Bags", "Leaf", "Peek", "Threshold"]
).agg(
    train_cr_mean=("Train CR", "mean"),
    val_cr_mean=("Val CR", "mean"),
    val_cr_median=("Val CR", "median"),
    val_cr_std=("Val CR", "std"),
    val_cr_min=("Val CR", "min"),
    val_cr_max=("Val CR", "max"),
    val_sharpe_mean=("Val Sharpe", "mean"),
    val_drawdown_mean=("Val Drawdown", "mean"),
    train_trades_mean=("Train Trades", "mean"),
    val_trades_mean=("Val Trades", "mean"),
    training_time_mean=("Training Time", "mean"),
    testing_time_mean=("Testing Time", "mean")
).reset_index()

summary = summary.sort_values(
    by="val_cr_mean", ascending=False
)

summary.to_csv(
    "strategy_grid_v2_summary.csv", index=False
)

print("\nTOP 20 CONFIGURATIONS")
print(summary.head(20).to_string(index=False))