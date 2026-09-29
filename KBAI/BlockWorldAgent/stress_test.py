from BlockWorldAgent import BlockWorldAgent
from collections import deque
import random


# ---------------------------------------------------------
# Convert a set of stacks into one standard representation.
# Stack order does not matter.
# ---------------------------------------------------------
def normalize(stacks):
    return tuple(sorted(tuple(stack) for stack in stacks if len(stack) > 0))


# ---------------------------------------------------------
# Generate a random arrangement using all supplied blocks.
# ---------------------------------------------------------
def random_arrangement(blocks):

    shuffled_blocks = blocks[:]
    random.shuffle(shuffled_blocks)

    number_of_stacks = random.randint(1, len(blocks))

    # One stack: easy special case
    if number_of_stacks == 1:
        return [shuffled_blocks]

    # Pick places where the shuffled list will be split
    split_points = sorted(
        random.sample(
            range(1, len(blocks)),
            number_of_stacks - 1
        )
    )

    stacks = []
    start = 0

    for split in split_points:
        stacks.append(shuffled_blocks[start:split])
        start = split

    stacks.append(shuffled_blocks[start:])

    return stacks


# ---------------------------------------------------------
# Independently verify that the moves returned by the agent
# are legal and actually reach the goal.
#
# We intentionally do NOT use the agent's apply_move()
# because we want the test to independently check the agent.
# ---------------------------------------------------------
def validate_solution(initial, goal, moves):

    current = [stack[:] for stack in initial]

    seen = {normalize(current)}

    for step_number, move in enumerate(moves, start=1):

        if not isinstance(move, tuple) or len(move) != 2:
            return False, f"Move {step_number} is not a valid tuple: {move}"

        block = move[0]
        destination = move[1]

        # Find the stack where the block is currently clear
        source_stack = None

        for stack in current:
            if stack[-1] == block:
                source_stack = stack
                break

        if source_stack is None:
            return False, (
                f"Move {step_number}: block {block} is not clear "
                f"and cannot be moved."
            )

        # -------------------------------------------------
        # Moving to the table
        # -------------------------------------------------
        if destination == "Table":

            source_stack.pop()

            if len(source_stack) == 0:
                current.remove(source_stack)

            current.append([block])

        # -------------------------------------------------
        # Moving onto another block
        # -------------------------------------------------
        else:

            if destination == block:
                return False, (
                    f"Move {step_number}: block {block} "
                    f"cannot be moved onto itself."
                )

            destination_stack = None

            for stack in current:
                if stack[-1] == destination:
                    destination_stack = stack
                    break

            if destination_stack is None:
                return False, (
                    f"Move {step_number}: destination block "
                    f"{destination} is not clear."
                )

            source_stack.pop()

            if len(source_stack) == 0:
                current.remove(source_stack)

            destination_stack.append(block)

        # Check for repeated states
        state = normalize(current)

        if state in seen:
            return False, (
                f"Move {step_number} returns to a previously seen state."
            )

        seen.add(state)

    # Did we actually reach the goal?
    if normalize(current) != normalize(goal):
        return False, (
            f"Agent did not reach goal.\n"
            f"Final: {current}\n"
            f"Goal:  {goal}"
        )

    return True, "Valid solution"


# =========================================================
# EXACT SHORTEST PATH
#
# Only use this for SMALL block counts.
# This BFS explores all possible states until it finds
# the goal and therefore gives us the real minimum moves.
# =========================================================

def generate_next_states(state):

    stacks = [list(stack) for stack in state]

    for source_index in range(len(stacks)):

        block = stacks[source_index][-1]

        # -------------------------------------------------
        # Move this block to the table.
        #
        # If it is already a one-block stack, moving it
        # "to the table" would not change the state.
        # -------------------------------------------------
        if len(stacks[source_index]) > 1:

            new_stacks = [stack[:] for stack in stacks]

            new_stacks[source_index].pop()
            new_stacks.append([block])

            yield normalize(new_stacks)

        # -------------------------------------------------
        # Move this block onto every other clear block.
        # -------------------------------------------------
        for destination_index in range(len(stacks)):

            if destination_index == source_index:
                continue

            new_stacks = [stack[:] for stack in stacks]

            moved_block = new_stacks[source_index].pop()

            new_stacks[destination_index].append(moved_block)

            if len(new_stacks[source_index]) == 0:
                del new_stacks[source_index]

            yield normalize(new_stacks)


def shortest_move_count(initial, goal):

    starting_state = normalize(initial)
    goal_state = normalize(goal)

    if starting_state == goal_state:
        return 0

    queue = deque()

    queue.append((starting_state, 0))

    seen = {starting_state}

    while queue:

        current_state, moves_so_far = queue.popleft()

        for next_state in generate_next_states(current_state):

            if next_state in seen:
                continue

            if next_state == goal_state:
                return moves_so_far + 1

            seen.add(next_state)

            queue.append(
                (next_state, moves_so_far + 1)
            )

    return None


# =========================================================
# RANDOM CORRECTNESS TEST
#
# This tests LARGE configurations too.
# It checks legality and whether the goal was reached,
# but does NOT prove optimality.
# =========================================================

def stress_test(trials_per_size=50):

    random.seed(7)

    block_counts = [3, 5, 8, 12, 20, 26]

    print("\n--- RANDOM CORRECTNESS TEST ---")

    for number_of_blocks in block_counts:

        blocks = [
            chr(ord("A") + i)
            for i in range(number_of_blocks)
        ]

        for test_number in range(1, trials_per_size + 1):

            initial = random_arrangement(blocks)
            goal = random_arrangement(blocks)

            agent = BlockWorldAgent()

            moves = agent.solve(initial, goal)

            valid, message = validate_solution(
                initial,
                goal,
                moves
            )

            if not valid:

                print("\nFAILED")
                print("Blocks:", number_of_blocks)
                print("Test:", test_number)
                print("Initial:", initial)
                print("Goal:", goal)
                print("Moves:", moves)
                print("Reason:", message)

                return

        print(
            f"{number_of_blocks} blocks: "
            f"{trials_per_size}/{trials_per_size} passed"
        )

    print("\nAll random correctness tests passed!")


# =========================================================
# RANDOM OPTIMALITY TEST
#
# Keep the number of blocks small because BFS becomes
# expensive as the problem grows.
# =========================================================

def optimality_test(trials_per_size=10):

    random.seed(17)

    print("\n--- RANDOM OPTIMALITY TEST ---")

    total_tests = 0
    optimal_tests = 0

    for number_of_blocks in range(3, 7):

        blocks = [
            chr(ord("A") + i)
            for i in range(number_of_blocks)
        ]

        for test_number in range(trials_per_size):

            initial = random_arrangement(blocks)
            goal = random_arrangement(blocks)

            agent = BlockWorldAgent()

            moves = agent.solve(initial, goal)

            valid, message = validate_solution(
                initial,
                goal,
                moves
            )

            if not valid:
                print("\nINVALID SOLUTION")
                print("Initial:", initial)
                print("Goal:", goal)
                print("Moves:", moves)
                print("Reason:", message)
                return

            minimum_moves = shortest_move_count(
                initial,
                goal
            )

            total_tests += 1

            if len(moves) == minimum_moves:
                optimal_tests += 1

            else:
                print("\nNON-OPTIMAL SOLUTION")
                print("Initial:", initial)
                print("Goal:", goal)
                print("Agent moves:", moves)
                print("Agent count:", len(moves))
                print("Minimum:", minimum_moves)

        print(f"{number_of_blocks} block tests complete")

    print()
    print(
        f"Optimal solutions: "
        f"{optimal_tests}/{total_tests}"
    )


if __name__ == "__main__":

    stress_test(trials_per_size=50)

    optimality_test(trials_per_size=10)