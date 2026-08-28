""""""
"""Assess a betting strategy.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 		  		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		 		  		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 		  		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		 		  		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		 		  		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		 		  		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		 		  		  		  		    	 		 		   		 		  
or edited.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		 		  		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		 		  		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 		  		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
Student Name: Robert Burrows (replace with your name)  		  	   		 		  		  		  		    	 		 		   		 		  
GT User ID: rburrows3 (replace with your User ID)  		  	   		 		  		  		  		    	 		 		   		 		  
GT ID: 904201091 (replace with your GT ID)  		  	   		 		  		  		  		    	 		 		   		 		  
"""

import numpy as np
import matplotlib.pyplot as plt


def author():
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 		  		  		  		    	 		 		   		 		  
    """
    return "rburrows3"  # replace tb34 with your Georgia Tech username.


def gtid():
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		 		  		  		  		    	 		 		   		 		  
    """
    return 904201091  # replace with your GT ID number


def get_spin_result(win_prob):
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		 		  		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		 		  		  		  		    	 		 		   		 		  
    """
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result


def play_episodes(test_defs):
    test_arrays = []
    for episodes, max_loss in test_defs:
        episode_results = np.zeros((episodes, 1001), dtype=int)
        for episode_number in range(episodes):
            limit = max_loss if max_loss is not None else np.inf
            episode_winnings = 0
            count = 1
            bet_amount = 1
            while count < 1001 and 80 > episode_winnings > -limit:
                won = get_spin_result(18 / 38)
                if won:
                    episode_winnings += bet_amount
                    # print(count, bet_amount, episode_winnings)
                    bet_amount = 1
                else:
                    episode_winnings -= bet_amount
                    # print(count, bet_amount, episode_winnings)
                    bet_amount *= 2
                if bet_amount > episode_winnings + limit:
                    bet_amount = episode_winnings + limit
                episode_results[episode_number, count] = episode_winnings
                count += 1
            episode_results[episode_number, count:] = episode_winnings
        test_arrays.append(episode_results)
    return test_arrays

def run_tests():
    test_defs = [(10, None), (1000, None), (1000, 256)]
    return play_episodes(test_defs)

def create_graphs(results_to_graph):
    create_basic_graph(results_to_graph[0], "martingale_sim.png") 
    create_mean_graph(results_to_graph[1], "martingale_mean_sim.png")
    create_median_graph(results_to_graph[1], "martingale_median_sim.png")
    create_mean_graph(results_to_graph[2], "martingale_mean_sim_2.png")
    create_median_graph(results_to_graph[2], "martingale_median_sim_2.png")

def create_basic_graph(graph_set, name):
    spins = np.arange(301)
    plt.figure()
    for episode in range(graph_set.shape[0]):
        plt.plot(spins, graph_set[episode, :301])
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel("spin")
    plt.ylabel("winnings")
    plt.title("Martingale Sim")
    plt.legend()
    plt.savefig(name)
    plt.close()

def create_mean_graph(graph_set, name):
    spins = np.arange(301)
    mean_results = np.mean(graph_set[:, :301], axis=0)
    std_dev = np.std(graph_set[:, :301], axis=0)
    plt.figure()
    plt.plot(spins, mean_results, label="Mean Winnings")
    plt.plot(spins, mean_results + std_dev, label="Positive Std Dev")
    plt.plot(spins, mean_results - std_dev, label="Negative Std Dev")
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel("spin")
    plt.ylabel("winnings")
    plt.title("Martingale Mean Sim")
    plt.legend()
    plt.savefig(name)
    plt.close()

def create_median_graph(graph_set, name):
    spins = np.arange(301)
    median_results = np.median(graph_set[:,:301], axis=0)
    std_dev = np.std(graph_set[:, :301], axis=0)
    plt.figure();
    plt.plot(spins, median_results, label="Median Winnings")
    plt.plot(spins, median_results + std_dev, label="Positive Std Dev")
    plt.plot(spins, median_results - std_dev, label="Negative Std Dev")
    plt.xlim(0,300)
    plt.ylim(-256,100)
    plt.xlabel("spin")
    plt.ylabel("winnings")
    plt.title("Martingale Median Sim")
    plt.legend()
    plt.savefig(name)
    plt.close()

def test_code():
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		 		  		  		  		    	 		 		   		 		  
    """
    win_prob = 18 / 38  # set appropriately to the probability of a win
    # np.random.seed(gtid())  # do this only once
    # print(get_spin_result(win_prob))
    # print(*run_tests(), sep="\n")
    results_to_graph = run_tests()
    create_graphs(results_to_graph)

    # print(run_tests()[0][:10, :24])# test the roulette spin
    # run_episodes()
    # add your code here to implement the experiments


if __name__ == "__main__":
    test_code()
