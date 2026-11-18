"""Local synthetic evaluation for the Monster Classification mini-project.

Place beside MonsterClassificationAgent.py and run: python3 test_agent.py
This is NOT a replica of Gradescope's hidden test generator.
"""

import random
from MonsterClassificationAgent import ATTRIBUTE_VALUES, MonsterClassificationAgent


SEED = 42
TRIALS = 100
TESTS_PER_TRIAL = 20
TRAINING_SIZES = (5, 10, 20, 40)  # Positive and negative examples EACH


def make_species(rng):
    """Independently choose a nonempty proper subset of values for each attribute."""
    allowed = {}
    for attribute, domain in ATTRIBUTE_VALUES.items():
        # Keep a mixture of narrow and broad attributes, while retaining
        # at least one forbidden value for generating negative examples.
        count = rng.randint(1, len(domain) - 1)
        allowed[attribute] = set(rng.sample(domain, count))
    return allowed


def is_species_member(monster, allowed):
    return all(value in allowed[attribute] for attribute, value in monster.items())


def make_positive(rng, allowed):
    return {attribute: rng.choice(tuple(sorted(values, key=str)))
            for attribute, values in allowed.items()}


def make_negative(rng, allowed):
    """Create a near-miss: change 1-3 allowed values to prohibited ones."""
    monster = make_positive(rng, allowed)
    changed = rng.sample(list(ATTRIBUTE_VALUES), rng.randint(1, 3))
    for attribute in changed:
        forbidden = [value for value in ATTRIBUTE_VALUES[attribute]
                     if value not in allowed[attribute]]
        monster[attribute] = rng.choice(forbidden)
    return monster


def original_baseline(agent, samples, monster):
    """The prior <=1 unknown rule, including our proven exclusions/constraints."""
    positive = agent.learn_positive_values(samples)
    excluded, constraints = agent.learn_negative_values(samples, positive)
    unknown = set()
    for attribute, value in monster.items():
        if value in excluded[attribute]:
            return False
        if value not in positive[attribute]:
            unknown.add((attribute, value))
    if any(constraint.issubset(unknown) for constraint in constraints):
        return False
    return len(unknown) <= 1


def evaluate():
    rng = random.Random(SEED)
    print(f"Seed: {SEED} | Trials per size: {TRIALS} | Test monsters per trial: {TESTS_PER_TRIAL}")
    print("Each test batch contains equal positive and negative monsters.\n")
    print(f"{'Train (+/-)':<13} {'Classifier':<14} {'Accuracy':>9} {'False +':>9} {'False -':>9}")
    print("-" * 61)

    for training_size in TRAINING_SIZES:
        stats = {name: {'correct': 0, 'fp': 0, 'fn': 0, 'total': 0}
                 for name in ('Baseline', 'Greedy')}

        for _ in range(TRIALS):
            allowed = make_species(rng)
            samples = [(make_positive(rng, allowed), True)
                       for _ in range(training_size)]
            samples += [(make_negative(rng, allowed), False)
                        for _ in range(training_size)]
            rng.shuffle(samples)

            tests = [(make_positive(rng, allowed), True)
                     for _ in range(TESTS_PER_TRIAL // 2)]
            tests += [(make_negative(rng, allowed), False)
                      for _ in range(TESTS_PER_TRIAL // 2)]
            rng.shuffle(tests)

            agent = MonsterClassificationAgent()
            for monster, expected in tests:
                assert is_species_member(monster, allowed) == expected
                predictions = {
                    'Baseline': original_baseline(agent, samples, monster),
                    'Greedy': agent.solve(samples, monster),
                }
                for name, prediction in predictions.items():
                    result = stats[name]
                    result['total'] += 1
                    result['correct'] += prediction == expected
                    result['fp'] += prediction and not expected
                    result['fn'] += (not prediction) and expected

        for name in ('Baseline', 'Greedy'):
            result = stats[name]
            accuracy = 100 * result['correct'] / result['total']
            print(f"{str(training_size) + '/' + str(training_size):<13} {name:<14} "
                  f"{accuracy:8.1f}% {result['fp']:9d} {result['fn']:9d}")
        print()

    print("False + = negative monster incorrectly accepted")
    print("False - = positive monster incorrectly rejected")
    print("Synthetic results are diagnostic, not a prediction of Gradescope accuracy.")


if __name__ == '__main__':
    evaluate()
