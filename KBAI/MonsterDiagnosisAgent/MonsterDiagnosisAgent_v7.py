"""Experimental hybrid: rolling cache + safe constraint-based pruning.

Keep the original three report versions unchanged. This is a fourth test version.
"""


class MonsterDiagnosisAgent:
    def solve(self, diseases, patient):
        values = {'+': 1, '-': -1, '0': 0}
        names = list(diseases)
        n = len(names)
        target = {vitamin: values[symbol] for vitamin, symbol in patient.items()}
        vectors = [
            {vitamin: values[symbol] for vitamin, symbol in diseases[name].items()
             if symbol != '0'}
            for name in names
        ]
        zero_totals = {vitamin: 0 for vitamin in patient}

        if self._matches(zero_totals, target):
            return []

        # Iterative deepening by *diagnosis size*, as in the original cache version.
        for size in range(1, n + 1):
            # Cache only one prefix depth at a time: prefix tuple -> vitamin totals.
            current_cache = {(): zero_totals}

            for depth in range(size):
                next_cache = {}
                remaining_after_add = size - depth - 1

                for prefix, totals in current_cache.items():
                    # Pruned prefixes never enter current_cache, so their
                    # descendants are never generated.
                    start = prefix[-1] + 1 if prefix else 0
                    last_possible = n - remaining_after_add

                    for idx in range(start, last_possible):
                        new_totals = totals.copy()
                        for vitamin, effect in vectors[idx].items():
                            new_totals[vitamin] += effect

                        if remaining_after_add == 0:
                            if self._matches(new_totals, target):
                                return [names[i] for i in (*prefix, idx)]
                        elif self._feasible(new_totals, target, remaining_after_add):
                            next_cache[(*prefix, idx)] = new_totals

                current_cache = next_cache
                if not current_cache and remaining_after_add > 0:
                    break

        return []

    @staticmethod
    def _matches(totals, target):
        for vitamin, value in totals.items():
            sign = (value > 0) - (value < 0)
            if sign != target[vitamin]:
                return False
        return True

    @staticmethod
    def _feasible(totals, target, remaining):
        # Same conservative pruning conditions as our backtracking version.
        # Any single future disease changes each vitamin by at most +/-1.
        for vitamin, value in totals.items():
            required = target[vitamin]
            if required == 1 and value + remaining <= 0:
                return False
            if required == -1 and value - remaining >= 0:
                return False
            if required == 0 and abs(value) > remaining:
                return False
        return True
