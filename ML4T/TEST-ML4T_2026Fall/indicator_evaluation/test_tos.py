import datetime as dt
import matplotlib.pyplot as plt

import TheoreticallyOptimalStrategy as tos
from marketsimcode import compute_portvals

trades = tos.testPolicy(
    symbol="JPM",
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 12, 31),
    sv=100000
)

portvals = compute_portvals(
    trades_df=trades,
    start_val=100000,
    commission=0.0,
    impact=0.0
)

print("First 10 portfolio values:")
print(portvals.head(10))

print("\nLast 10 portfolio values:")
print(portvals.tail(10))

print("\nStarting value:", portvals.iloc[0, 0])
print("Ending value:", portvals.iloc[-1, 0])

print("\nMinimum daily change:")
print(portvals.iloc[:, 0].diff().dropna().min())

benchmark_trades = trades.copy()
benchmark_trades[:] = 0
benchmark_trades.iloc[0, 0] = 1000

benchmark_vals = compute_portvals(
    trades_df=benchmark_trades,
    start_val=100000,
    commission=0.0,
    impact=0.0
)

print("Benchmark starting value:", benchmark_vals.iloc[0, 0])
print("Benchmark ending value:", benchmark_vals.iloc[-1, 0])


def portfolio_stats(portvals):
    values = portvals.iloc[:, 0]

    daily_returns = values.pct_change().dropna()

    cumulative_return = values.iloc[-1] / values.iloc[0] - 1
    std_daily_return = daily_returns.std()
    mean_daily_return = daily_returns.mean()

    return cumulative_return, std_daily_return, mean_daily_return


benchmark_stats = portfolio_stats(benchmark_vals)
tos_stats = portfolio_stats(portvals)

print("\nPerformance Statistics")
print(f"{'Metric':<25} {'Benchmark':>15} {'TOS':>15}")

for label, benchmark, tos in zip(
    ["Cumulative Return", "Std Daily Return", "Mean Daily Return"],
    benchmark_stats,
    tos_stats
):
    print(f"{label:<25} {benchmark:>15.6f} {tos:>15.6f}")

benchmark_normalized = benchmark_vals / benchmark_vals.iloc[0, 0]
tos_normalized = portvals / portvals.iloc[0, 0]

plt.figure(figsize=(10, 6))

plt.plot(
    benchmark_normalized.index,
    benchmark_normalized.iloc[:, 0],
    color="purple",
    label="Benchmark"
)

plt.plot(
    tos_normalized.index,
    tos_normalized.iloc[:, 0],
    color="red",
    label="Theoretically Optimal Strategy"
)

plt.title("JPM: Theoretically Optimal Strategy vs. Benchmark")
plt.xlabel("Date")
plt.ylabel("Normalized Portfolio Value")
plt.legend()
plt.grid(True)

plt.savefig("tos_comparison.png", bbox_inches="tight")
plt.close()