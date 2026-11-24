import datetime as dt
import StrategyLearner as sl
import indicators as ind

learner = sl.StrategyLearner(
    impact=0.005,
    commission=9.95
)

prices, features = ind.get_features(
    "JPM",
    dt.datetime(2008, 1, 1),
    dt.datetime(2009, 12, 31)
)

labels = learner.get_labels(prices)

print("LABEL COUNTS")
print(labels.value_counts(dropna=False))

print("\nLABEL DISTRIBUTION")
print(labels.value_counts(normalize=True))

print("\nTOTAL OBSERVATIONS")
print(len(labels))

print("\nVALID TRAINING LABELS")
print(labels.notna().sum())

print("\nLAST 10 LABELS")
print(labels.tail(10))

print("\nMARKET IMPACT ANALYSIS")

for impact in [0.0, 0.005, 0.01, 0.02, 0.05]:

    learner.impact = impact

    labels = learner.get_labels(prices)

    print(f"\nImpact: {impact}")
    print(labels.value_counts().sort_index())