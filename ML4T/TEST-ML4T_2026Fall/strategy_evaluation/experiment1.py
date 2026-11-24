import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

import ManualStrategy as ms
import StrategyLearner as sl
import marketsimcode as msc


def author():
    return "rburrows3"


def study_group():
    return "rburrows3"


def test_strategies(manual, learner, symbol, sd, ed, sv, commission, impact):


    manual_trades = manual.testPolicy(symbol, sd, ed, sv)
    learner_trades = learner.testPolicy(symbol, sd, ed, sv)
    benchmark_trades = msc.get_benchmark(symbol, sd,ed)

    manual_values = msc.compute_portvals(manual_trades, sv, commission, impact)
    learner_values = msc.compute_portvals(learner_trades, sv, commission, impact)
    benchmark_values = msc.compute_portvals(benchmark_trades, sv, commission, impact)

    manual_stats = msc.get_stats(manual_values)
    learner_stats = msc.get_stats(learner_values)
    benchmark_stats = msc.get_stats(benchmark_values)

    stats = pd.DataFrame({"Manual Strategy": manual_stats, "Strategy Learner": learner_stats,"Benchmark": benchmark_stats})

    return manual_values, learner_values, benchmark_values, stats

def get_strategy_chart(manual_values, learner_values, benchmark_values, title, filename):

    manual_normalized = manual_values.iloc[:,0]/manual_values.iloc[0,0]
    learner_normalized = learner_values.iloc[:,0]/learner_values.iloc[0,0]
    benchmark_normalized = benchmark_values.iloc[:,0]/benchmark_values.iloc[0,0]


    fig, ax = plt.subplots(figsize=(12,6))

    ax.plot(benchmark_normalized, color="purple", label="Benchmark")
    ax.plot(manual_normalized, color="red", label="Manual Strategy")
    ax.plot(learner_normalized, color="green", label="Strategy Learner")


    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Portfolio Value")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("./images/" + filename, dpi=150)
    plt.close()

def perform_experiment(symbol, periods, sv, commission, impact):
    manual = ms.ManualStrategy(impact=impact, commission=commission)
    learner = sl.StrategyLearner(impact=impact, commission=commission)

    sd,ed = periods["In-Sample"]

    learner.add_evidence(symbol, sd,ed,sv)


    all_stats = {}
    for name, (sd, ed) in periods.items():

        manual_values, learner_values, benchmark_values, stats = test_strategies(
            manual, learner, symbol, sd, ed, sv, commission, impact)
        
        all_stats[name] = stats

        get_strategy_chart(manual_values, learner_values, benchmark_values, f"Strategy Comparison ({name})", f"Experiment_1_{name.lower()}.png")

        print(f"\nExperiment 1: {name}")
        print(stats.to_string(float_format="%.6f"))

    combined_stats = pd.concat(all_stats, axis=1)

    combined_stats.to_csv("experiment1_stats.csv",float_format="%.6f")