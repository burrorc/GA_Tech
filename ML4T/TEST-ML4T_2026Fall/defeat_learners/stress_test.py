import time
import numpy as np

from gen_data import best_4_lin_reg, best_4_dt
from LinRegLearner import LinRegLearner
from DTLearner import DTLearner


def test_generator(generator, better_class, worse_class, seed):
    x, y = generator(seed=seed)

    num_samples = x.shape[0]
    cutoff = int(num_samples * 0.6)

    wins = 0

    for _ in range(15):
        permutation = np.random.permutation(num_samples)

        train_x = x[permutation[:cutoff]]
        train_y = y[permutation[:cutoff]]

        test_x = x[permutation[cutoff:]]
        test_y = y[permutation[cutoff:]]

        better = better_class()
        worse = worse_class()

        better.add_evidence(train_x, train_y)
        worse.add_evidence(train_x, train_y)

        better_pred = better.query(test_x)
        worse_pred = worse.query(test_x)

        better_err = np.linalg.norm(test_y - better_pred)
        worse_err = np.linalg.norm(test_y - worse_pred)

        if better_err < 0.9 * worse_err:
            wins += 1

    return wins


num_seeds = 50

linreg_results = []
dt_results = []

start = time.perf_counter()

for seed in range(num_seeds):

    if seed % 5 == 0:
        elapsed = time.perf_counter() - start
        print(f"Seed {seed}/{num_seeds} - {elapsed:.1f}s elapsed")

    linreg_results.append(
        test_generator(
            best_4_lin_reg,
            LinRegLearner,
            DTLearner,
            seed
        )
    )

    dt_results.append(
        test_generator(
            best_4_dt,
            DTLearner,
            LinRegLearner,
            seed
        )
    )


print("\nLINEAR REGRESSION")
print("Minimum wins:", min(linreg_results))
print("Average wins:", np.mean(linreg_results))
print("Passing seeds:", sum(x >= 10 for x in linreg_results), "/", num_seeds)

print("\nDECISION TREE")
print("Minimum wins:", min(dt_results))
print("Average wins:", np.mean(dt_results))
print("Passing seeds:", sum(x >= 10 for x in dt_results), "/", num_seeds)

print("\nTotal time:", time.perf_counter() - start)