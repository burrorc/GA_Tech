import datetime as dt
import StrategyLearner as sl
import time

learner = sl.StrategyLearner(
    verbose=True,
    impact=0.005,
    commission=9.95
)

start = time.perf_counter()

learner.add_evidence(
    symbol="JPM",
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 12, 31),
    sv=100000
)

elapsed = time.perf_counter() - start

print(f"Training time: {elapsed:.6f} seconds")