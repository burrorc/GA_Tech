"""Compare basic Q-Learning and Dyna-Q on the same navigation world.

Save in qlearning_robot/ beside QLearner.py and testqlearner.py.
Run: PYTHONPATH=../:. python compare_dyna.py
"""

import random
import time
from pathlib import Path

import numpy as np
import QLearner as ql
from testqlearner import discretize, getgoalpos, getrobotpos, movebot


WORLD_FILE = Path(__file__).resolve().parent / "testworlds" / "world01.csv"
EPOCHS = 50
SEEDS = (5, 17, 29, 41, 53)
MAX_STEPS = 10000


def run_training(world, dyna, seed):
    # Same starting seed and parameters for both configurations.
    random.seed(seed)
    np.random.seed(seed)
    learner = ql.QLearner(
        num_states=100,
        num_actions=4,
        alpha=0.2,
        gamma=0.9,
        rar=0.5,
        radr=0.99,
        dyna=dyna,
        verbose=False,
    )

    startpos = getrobotpos(world)
    goalpos = getgoalpos(world)
    rewards = []
    start_time = time.perf_counter()

    for epoch in range(EPOCHS):
        data = world.copy()
        robopos = startpos
        action = learner.querysetstate(discretize(robopos))
        total_reward = 0

        for step in range(MAX_STEPS):
            newpos, reward = movebot(data, robopos, action)
            action = learner.query(discretize(newpos), reward)

            # Match the supplied navigation test's map-marking behavior.
            if data[robopos] != 6:
                data[robopos] = 4
            if data[newpos] != 6:
                data[newpos] = 2

            robopos = newpos
            total_reward += reward
            if robopos == goalpos:
                break

        rewards.append(total_reward)

    elapsed = time.perf_counter() - start_time
    return {
        "median": float(np.median(rewards)),
        "early": float(np.median(rewards[:10])),
        "late": float(np.median(rewards[-10:])),
        "seconds": elapsed,
    }


def main():
    world = np.loadtxt(WORLD_FILE, delimiter=",")
    results = {0: [], 200: []}

    print(f"World: {WORLD_FILE.name} | Epochs per run: {EPOCHS}")
    print("Higher (less negative) reward is better.\n")
    print(f"{'Seed':>6} {'Dyna':>6} {'Median':>10} {'First 10':>10} {'Last 10':>10} {'Seconds':>10}")
    print("-" * 58)

    for seed in SEEDS:
        for dyna in (0, 200):
            result = run_training(world, dyna, seed)
            results[dyna].append(result)
            print(
                f"{seed:>6} {dyna:>6} {result['median']:>10.1f} "
                f"{result['early']:>10.1f} {result['late']:>10.1f} "
                f"{result['seconds']:>10.3f}"
            )

    print("\nAverage across seeds (each run's median reward):")
    for dyna in (0, 200):
        avg_reward = np.mean([item["median"] for item in results[dyna]])
        avg_time = np.mean([item["seconds"] for item in results[dyna]])
        print(f"Dyna={dyna:>3}: average median reward = {avg_reward:.1f}; mean runtime = {avg_time:.3f}s")

    differences = [
        dyna_result["median"] - basic_result["median"]
        for basic_result, dyna_result in zip(results[0], results[200])
    ]
    print(f"Dyna minus basic: average reward difference = {np.mean(differences):+.1f}")
    print("Positive means Dyna achieved higher rewards on average.")
    print("Note: shared seeds aid reproducibility, but the two runs diverge as they learn.")


if __name__ == "__main__":
    main()
