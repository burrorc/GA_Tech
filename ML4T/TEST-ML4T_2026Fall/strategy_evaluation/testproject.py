import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import ManualStrategy as ms
import marketsimcode as msc
import experiment1 as exp1
import experiment2 as exp2

def author():
    return "rburrows3"


def study_group():
    return "rburrows3"

def test_manual(symbol, sd, ed, sv, commission, impact):

    manual = ms.ManualStrategy(impact=impact, commission=commission)

    manual_trades = manual.testPolicy(symbol, sd, ed, sv)
    benchmark_trades = msc.get_benchmark(symbol, sd,ed)

    manual_values = msc.compute_portvals(manual_trades, sv, commission, impact)
    benchmark_values = msc.compute_portvals(benchmark_trades, sv, commission, impact)

    manual_stats = msc.get_stats(manual_values)
    benchmark_stats = msc.get_stats(benchmark_values)

    stats = pd.DataFrame({"Manual Strategy": manual_stats, "Benchmark": benchmark_stats})

    return manual_trades, manual_values, benchmark_values, stats


def get_manual_chart(manual_values, benchmark_values, trades, title, filename):

    manual_normalized = manual_values.iloc[:,0]/manual_values.iloc[0,0]
    benchmark_normalized = benchmark_values.iloc[:,0]/benchmark_values.iloc[0,0]

    holdings = trades.iloc[:,0].cumsum()

    prev_holdings = holdings.shift(1).fillna(0)

    longs = holdings.index[(holdings ==1000) & (prev_holdings != 1000)]
    shorts = holdings.index[(holdings ==-1000) & (prev_holdings != -1000)]


    fig, ax = plt.subplots(figsize=(12,6))

    ax.plot(benchmark_normalized, color="purple", label="Benchmark")
    ax.plot(manual_normalized, color="red", label="Manual Strategy")



    for i, date in enumerate(longs):
        ax.axvline(date, color="blue", alpha=0.5, label="Long Entry" if i ==0 else None)

    for i, date in enumerate(shorts):
            ax.axvline(date, color="black", alpha=0.5, label="Short Entry" if i ==0 else None)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Portfolio Value")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("./images/" + filename, dpi=150)
    plt.close()

if __name__ == "__main__":
    np.random.seed(904201091)

    symbol = "JPM"
    sv = 100000
    commission = 9.95
    impact = 0.005

    periods = {
        "In-Sample": (
            dt.datetime(2008, 1, 1),
            dt.datetime(2009, 12, 31)
        ),
        "Out-of-Sample": (
            dt.datetime(2010, 1, 1),
            dt.datetime(2011, 12, 31)
        )
    }

    all_stats = {}
    for name, (sd, ed) in periods.items():

        trades, manual_values, benchmark_values, stats = test_manual(
            symbol, sd, ed, sv, commission, impact
        )
        all_stats[name] = stats

        print(f"\n{name}")
        print(stats.to_string(float_format="%.6f"))
        print(f"Transactions: {(trades[symbol] != 0).sum()}")

        get_manual_chart(manual_values, benchmark_values, trades, f"Manual Strategy v Benchmark ({name})",f"manual_{name.lower()}.png" )

    combined_stats = pd.concat(all_stats, axis=1)

    combined_stats.to_csv("manual_strategy_stats.csv",float_format="%.6f")

    exp1.perform_experiment(symbol, periods, sv, commission, impact)
    
    sd, ed = periods["In-Sample"]
    exp2.perform_experiment(symbol, sd, ed, sv)