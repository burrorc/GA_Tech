"""Benchmark Mini-Project 5 without modifying MonsterDiagnosisAgent.py.

Place this file beside MonsterDiagnosisAgent.py, then run:
    python3 benchmark_monster.py

Optional heavier search (can take much longer):
    python3 benchmark_monster.py --stress
"""

import argparse
import random
import statistics
import time
import tracemalloc
from itertools import combinations

from MonsterDiagnosisAgent_v7 import MonsterDiagnosisAgent

VITAMINS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TO_NUMBER = {"+": 1, "-": -1, "0": 0}
TO_SYMBOL = {1: "+", -1: "-", 0: "0"}


def sign(number):
    return (number > 0) - (number < 0)


def patient_from_selection(diseases, selected):
    """Independently construct an observed patient from selected diseases."""
    totals = {vitamin: 0 for vitamin in VITAMINS}
    for name in selected:
        for vitamin, symbol in diseases[name].items():
            totals[vitamin] += TO_NUMBER[symbol]
    return {vitamin: TO_SYMBOL[sign(total)] for vitamin, total in totals.items()}


def make_case(number_of_diseases, planted_count, seed):
    """Produce deterministic, sparse diseases (3-6 affected vitamins each).

    The planted_count is how many diseases CREATE the patient; it may be
    larger than the actual minimum diagnosis size.
    """
    rng = random.Random(seed)
    diseases = {}
    for i in range(number_of_diseases):
        symptoms = {vitamin: "0" for vitamin in VITAMINS}
        for vitamin in rng.sample(VITAMINS, rng.randint(3, 6)):
            symptoms[vitamin] = rng.choice(("+", "-"))
        diseases[f"Disease_{i:02d}"] = symptoms

    selected = rng.sample(list(diseases), planted_count)
    patient = patient_from_selection(diseases, selected)
    return diseases, patient, selected


def is_valid(diseases, patient, result):
    return (isinstance(result, list)
            and len(result) == len(set(result))
            and all(isinstance(name, str) and name in diseases for name in result)
            and patient_from_selection(diseases, result) == patient)


def smallest_size_bruteforce(diseases, patient):
    """Independent optimality verification for small disease catalogs ONLY."""
    names = list(diseases)
    for k in range(len(names) + 1):
        for group in combinations(names, k):
            if patient_from_selection(diseases, group) == patient:
                return k
    return None


def run_case(label, disease_count, planted_count, seed, repetitions):
    diseases, patient, planted = make_case(disease_count, planted_count, seed)
    times_ms = []
    # peaks_mib = []
    result = None
    for _ in range(repetitions):
        agent = MonsterDiagnosisAgent()
        start = time.perf_counter()
        # tracemalloc.start()
        result = agent.solve(diseases, patient)
        # current, peak = tracemalloc.get_traced_memory()
        # tracemalloc.stop()
        # peaks_mib.append(peak / (1024 ** 2))
        times_ms.append((time.perf_counter() - start) * 1000)
        
    # print(f"Median peak memory: {statistics.median(peaks_mib):.3f} MiB")

    valid = is_valid(diseases, patient, result)
    optimum = smallest_size_bruteforce(diseases, patient) if disease_count <= 10 else None
    optimal = (len(result) == optimum) if valid and optimum is not None else None
    status = "PASS" if valid and optimal is not False else "FAIL"
    result_size = len(result) if isinstance(result, list) else "n/a"
    check = "verified" if optimal is True else ("NOT MINIMAL" if optimal is False else "not checked")
    print(f"{label:<13} {disease_count:>3} {planted_count:>7} {str(result_size):>7} "
          f"{statistics.median(times_ms):>12.3f}  {status:<5}  {check}")
    if not valid:
        print(f"  Invalid result: {result!r}; planted diseases: {planted}")
    return status == "PASS"


def main():
    parser = argparse.ArgumentParser(description="Benchmark MonsterDiagnosisAgent")
    parser.add_argument("--stress", action="store_true",
                        help="include potentially slow cases with larger planted diagnoses")
    parser.add_argument("--repetitions", type=int, default=3,
                        help="timed runs per case (default 3)")
    args = parser.parse_args()
    if args.repetitions < 1:
        parser.error("--repetitions must be at least 1")

    cases = [
        ("Small", 5, 2, 101),
        ("Medium", 10, 2, 102),
        ("Medium+", 10, 3, 103),
        ("Large", 15, 3, 104),
        ("Larger", 20, 4, 105),
        ("Maximum", 24, 4, 106),
    ]
    if args.stress:
        cases += [
            ("Stress-5", 24, 5, 107),
            ("Stress-6", 24, 6, 108),
        ]

    print("Monster Diagnosis Benchmark (median wall-clock time; lower is faster)")
    print("The 'planted' count creates the patient; the true minimum may be smaller.")
    print("Optimality is independently verified only for catalogs with <= 10 diseases.")
    print(f"{'Case':<13} {'N':>3} {'Planted':>7} {'Found':>7} {'Median ms':>12}  {'Valid':<5}  Optimality")
    print("-" * 83)
    passed = 0
    for label, n, count, seed in cases:
        passed += run_case(label, n, count, seed, args.repetitions)
    print("-" * 83)
    print(f"Valid cases: {passed}/{len(cases)}")
    print("Note: Large-case PASS verifies symptom coverage, not guaranteed minimality.")


if __name__ == "__main__":
    main()
