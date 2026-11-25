import pandas as pd
import matplotlib.pyplot as plt

import StrategyLearner as sl
import marketsimcode as msc


def author():
    return "rburrows3"


def study_group():
    return "rburrows3"


def test_impact(symbol, sd, ed, sv, impacts):

    results = []
    commission = 0.0

    for impact in impacts:

        learner = sl.StrategyLearner(impact=impact, commission=commission)
        learner.add_evidence(symbol, sd, ed,sv)

        trades = learner.testPolicy(symbol, sd, ed, sv)

        portvals = msc.compute_portvals(trades, sv, commission, impact)

        
        
        stats = msc.get_stats(portvals)
        holdings = trades[symbol].cumsum()

        results.append({
            "Impact": impact,
            "CR": stats["CR"],
            "Transactions": (trades[symbol] != 0).sum(),
            "Shares Traded": trades[symbol].abs().sum(),
            "Long Days": (holdings == 1000).sum(),
            "Short Days": (holdings == -1000).sum(),
            "Cash Days": (holdings == 0).sum(),
            "SDDR": stats["SDDR"]
        })

    return pd.DataFrame(results)


def get_impact_chart(results, metric, ylabel, title, filename):
    fig, ax = plt.subplots(figsize=(12,6))

    impacts = [f"{impact:.1%}" for impact in results["Impact"]]

    ax.bar(impacts, results[metric])

    ax.set_title(title)
    ax.set_xlabel("Market Impact")
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig("./images/"+filename, dpi=150)
    plt.close(fig)

def perform_experiment(symbol, sd, ed, sv):

    impacts = [0.0, 0.005,0.01, 0.02, 0.05]

    results = test_impact(symbol, sd, ed, sv, impacts)

    get_impact_chart(results, "CR", "Cumulative Return", "Market Impact on Cumulative Return", "Experiment_2_returns.png")

    get_impact_chart(results, "Transactions", "Num of Transactions", "Market Impact on Trading Frequency", "Experiment_2_transactions.png")


    return results

