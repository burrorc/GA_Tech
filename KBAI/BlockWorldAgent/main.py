# # from BlockWorldAgent import BlockWorldAgent

# # def test():
# #     #This will test your BlockWorldAgent
# # 	#with eight initial test cases.
# #     test_agent = BlockWorldAgent()

# # #     initial = [
# # #     ["A", "B", "C"],
# # #     ["D", "E", "X"]
# # # ]
# # #     goal = [
# # #     ["D", "E", "B", "X"],
# # #     ["A", "C"]
# # # ]
# # #     print("Result:", test_agent.solve(initial, goal))

# #     initial_arrangement_1 = [["A", "B", "C"], ["D", "E"]]
# #     goal_arrangement_1 = [["A", "C"], ["D", "E", "B"]]
# #     goal_arrangement_2 = [["A", "B", "C", "D", "E"]]
# #     goal_arrangement_3 = [["D", "E", "A", "B", "C"]]
# #     goal_arrangement_4 = [["C", "D"], ["E", "A", "B"]]

# #     print(test_agent.solve(initial_arrangement_1, goal_arrangement_1))
# #     print(test_agent.solve(initial_arrangement_1, goal_arrangement_2))
# #     print(test_agent.solve(initial_arrangement_1, goal_arrangement_3))
# #     print(test_agent.solve(initial_arrangement_1, goal_arrangement_4))

# #     initial_arrangement_2 = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
# #     goal_arrangement_5 = [["A", "B", "C", "D", "E", "F", "G", "H", "I"]]
# #     goal_arrangement_6 = [["I", "H", "G", "F", "E", "D", "C", "B", "A"]]
# #     goal_arrangement_7 = [["H", "E", "F", "A", "C"], ["B", "D"], ["G", "I"]]
# #     goal_arrangement_8 = [["F", "D", "C", "I", "G", "A"], ["B", "E", "H"]]

# #     print(test_agent.solve(initial_arrangement_2, goal_arrangement_5))
# #     print(test_agent.solve(initial_arrangement_2, goal_arrangement_6))
# #     print(test_agent.solve(initial_arrangement_2, goal_arrangement_7))
# #     print(test_agent.solve(initial_arrangement_2, goal_arrangement_8))

# # if __name__ == "__main__":
# #     test()

# from BlockWorldAgent import BlockWorldAgent


# def test():
#     test_agent = BlockWorldAgent()

#     # ---------------------------------------------------------
#     # Gradescope regression test 1
#     # Expected: valid solution in 21 moves or fewer
#     # ---------------------------------------------------------
#     initial_1 = [
#         ["N", "I", "A", "F"],
#         ["L", "G", "D", "B", "O", "H", "C", "M", "P", "J"],
#         ["K", "E"]
#     ]

#     goal_1 = [
#         ["I", "F"],
#         ["O", "J", "C", "A"],
#         ["K", "H", "M"],
#         ["G", "B"],
#         ["L", "P", "E"],
#         ["D", "N"]
#     ]

#     result_1 = test_agent.solve(initial_1, goal_1)

#     print("----- TEST 1 -----")
#     print("Moves:", result_1)
#     print("Move count:", len(result_1))
#     print("Expected: <= 21")
#     print()


#     # ---------------------------------------------------------
#     # Gradescope regression test 2
#     # Expected: valid solution in 17 moves or fewer
#     # ---------------------------------------------------------
#     initial_2 = [
#         ["I", "J", "E", "F", "D", "A"],
#         ["H", "C", "L"],
#         ["G", "Q", "M"],
#         ["P"],
#         ["O", "K", "N", "B"]
#     ]

#     goal_2 = [
#         ["I", "J", "F", "D", "A"],
#         ["H", "P"],
#         ["M", "G"],
#         ["E", "K"],
#         ["B", "O"],
#         ["L"],
#         ["N"],
#         ["Q", "C"]
#     ]

#     result_2 = test_agent.solve(initial_2, goal_2)

#     print("----- TEST 2 -----")
#     print("Moves:", result_2)
#     print("Move count:", len(result_2))
#     print("Expected: <= 17")
#     print()


# if __name__ == "__main__":
#     test()

from BlockWorldAgent.BlockWorldAgent_FINAL import BlockWorldAgent

import random
import time
import statistics


def random_arrangement(blocks):
    blocks = blocks[:]
    random.shuffle(blocks)

    number_of_stacks = random.randint(1, len(blocks))

    if number_of_stacks == 1:
        return [blocks]

    cut_points = sorted(
        random.sample(
            range(1, len(blocks)),
            number_of_stacks - 1
        )
    )

    stacks = []
    start = 0

    for cut in cut_points:
        stacks.append(blocks[start:cut])
        start = cut

    stacks.append(blocks[start:])

    return stacks


def benchmark(block_count, test_count=100):

    blocks = [
        chr(ord("A") + i)
        for i in range(block_count)
    ]

    times = []
    move_counts = []

    for i in range(test_count):

        initial = random_arrangement(blocks)
        goal = random_arrangement(blocks)

        agent = BlockWorldAgent()

        start_time = time.perf_counter()

        moves = agent.solve(initial, goal)

        end_time = time.perf_counter()

        times.append(end_time - start_time)
        move_counts.append(len(moves))

    average_time = statistics.mean(times)
    median_time = statistics.median(times)
    max_time = max(times)
    average_moves = statistics.mean(move_counts)

    print(f"{block_count} blocks")
    print(f"  Tests:          {test_count}")
    print(f"  Average time:   {average_time:.6f} seconds")
    print(f"  Median time:    {median_time:.6f} seconds")
    print(f"  Maximum time:   {max_time:.6f} seconds")
    print(f"  Average moves:  {average_moves:.2f}")
    print()


def test():

    random.seed(42)

    print("----- BLOCK WORLD TIMING TEST -----")
    print()

    for block_count in [5, 10, 15, 20, 26]:
        benchmark(block_count, 100)


if __name__ == "__main__":
    test()