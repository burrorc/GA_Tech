""""""  		  	   		 		  		  		  		    	 		 		   		 		  
"""  		  	   		 		  		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
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
"""  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import math  		  	   		 		  		  		  		    	 		 		   		 		  
import sys  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import numpy as np
import matplotlib.pyplot as plt  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import DTLearner as dt  
import BagLearner as bl	
import RTLearner as rt
import time	  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:  		  	   		 		  		  		  		    	 		 		   		 		  
        print("Usage: python testlearner.py <filename>")  		  	   		 		  		  		  		    	 		 		   		 		  
        sys.exit(1)  
        	
    inf = open(sys.argv[1])

    lines = inf.readlines()[1:] 
    

    data = np.array(
        [list(map(float, s.strip().split(",")[1:])) for s in lines]
    )

    
    np.random.shuffle(data)	  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing  		  	   		 		  		  		  		    	 		 		   		 		  
    train_rows = int(0.6 * data.shape[0])  		  	   		 		  		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # separate out training and testing data  		  	   		 		  		  		  		    	 		 		   		 		  
    train_x = data[:train_rows, 0:-1]  		  	   		 		  		  		  		    	 		 		   		 		  
    train_y = data[:train_rows, -1]  		  	   		 		  		  		  		    	 		 		   		 		  
    test_x = data[train_rows:, 0:-1]  		  	   		 		  		  		  		    	 		 		   		 		  
    test_y = data[train_rows:, -1]  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"{test_x.shape}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"{test_y.shape}")

    leaf_sizes = np.arange(1,101)
    in_sample = np.zeros(leaf_sizes.shape[0])
    out_sample = np.zeros(leaf_sizes.shape[0])
    bag_in_sample = np.zeros(leaf_sizes.shape[0])
    bag_out_sample = np.zeros(leaf_sizes.shape[0])  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    

    for i in range(leaf_sizes.shape[0]):
        leaf_size = leaf_sizes[i]  		  	   		 		  		  		  		    	 		 		   		 		
        learner = dt.DTLearner(leaf_size=leaf_size, verbose=False)
        learner.add_evidence(train_x, train_y)
        prediction_i = learner.query(train_x)
        rmse_i = math.sqrt(((train_y - prediction_i) ** 2).sum() / train_y.shape[0])
        in_sample[i] = rmse_i
        prediction_o = learner.query(test_x)
        rmse_o = math.sqrt(((test_y - prediction_o) ** 2).sum() / test_y.shape[0])
        out_sample[i] = rmse_o
  		  	   		 		  		  		  		    	 		 		   		 		  
    # evaluate in sample  		  	   		 		  		  		  		    	 		 		   		 		  
    pred_y = learner.query(train_x)  # get the predictions  		  	   		 		  		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])  		  	   		 		  		  		  		    	 		 		   		 		  
    print()  		  	   		 		  		  		  		    	 		 		   		 		  
    print("In sample results")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		 		  		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=train_y)  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # evaluate out of sample  		  	   		 		  		  		  		    	 		 		   		 		  
    pred_y = learner.query(test_x)  # get the predictions  		  	   		 		  		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])  		  	   		 		  		  		  		    	 		 		   		 		  
    print()  		  	   		 		  		  		  		    	 		 		   		 		  
    print("Out of sample results")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		  	   		 		  		  		  		    	 		 		   		 		  
    c = np.corrcoef(pred_y, y=test_y)  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")

    


    best_index = np.argmin(out_sample)
    print("Best leaf size:", leaf_sizes[best_index])
    print("Lowest out-of-sample RMSE:", out_sample[best_index])


    plt.figure()

    plt.plot(leaf_sizes, in_sample, label="In-Sample RMSE")
    plt.plot(leaf_sizes, out_sample, label="Out-of-Sample RMSE")

    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.title("Experiment 1 - DTLearner Overfitting")

    plt.legend()

    plt.savefig("./images/experiment1.png")
    plt.close() 

    for i in range(leaf_sizes.shape[0]):
        leaf_size = leaf_sizes[i]
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size": leaf_size}, bags=20, boost=False, verbose=False)
        learner.add_evidence(train_x, train_y)
        prediction_i = learner.query(train_x)
        rmse_i = math.sqrt(((train_y - prediction_i) ** 2).sum() / train_y.shape[0])
        bag_in_sample[i] = rmse_i
        prediction_o = learner.query(test_x)
        rmse_o = math.sqrt(((test_y - prediction_o) ** 2).sum() / test_y.shape[0])
        bag_out_sample[i] = rmse_o


    best_bag_index = np.argmin(bag_out_sample)
    print("Best bag leaf size:", leaf_sizes[best_bag_index])
    print("Lowest out-of-sample RMSE for bag learner:", bag_out_sample[best_bag_index])

    plt.figure()

    plt.plot(leaf_sizes, bag_in_sample, label="In-Sample RMSE")
    plt.plot(leaf_sizes, bag_out_sample, label="Out-of-Sample RMSE")

    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.title("Experiment 2 - BagLearner Overfitting")

    plt.legend()

    plt.savefig("./images/experiment2.png")
    plt.close()

    dt_mae = np.zeros(leaf_sizes.shape[0])
    rt_mae = np.zeros(leaf_sizes.shape[0])

    dt_train_time = np.zeros(leaf_sizes.shape[0])
    rt_train_time = np.zeros(leaf_sizes.shape[0])

    

    for i in range(leaf_sizes.shape[0]):
            leaf_size = leaf_sizes[i]
            dt_time_total = 0

            for run in range(10):
                dt_learner = dt.DTLearner(leaf_size=leaf_size, verbose=False)
                start_time_dt = time.perf_counter()
                dt_learner.add_evidence(train_x, train_y)
                end_time_dt = time.perf_counter()
                dt_time_total += end_time_dt - start_time_dt
            dt_train_time[i] = dt_time_total / 10
    
            prediction_dt = dt_learner.query(test_x)
            dt_mae[i] = np.mean(np.abs(test_y - prediction_dt))

            rt_time_total = 0
            rt_mae_total = 0
    
            for run in range(10):
                rt_learner = rt.RTLearner(leaf_size=leaf_size, verbose=False)
                start_time_rt = time.perf_counter()
                rt_learner.add_evidence(train_x, train_y)
                end_time_rt = time.perf_counter()
                rt_time_total += end_time_rt - start_time_rt

                prediction_rt = rt_learner.query(test_x)
                current_mae = np.mean(np.abs(test_y - prediction_rt))
                rt_mae_total += current_mae
            rt_train_time[i] = rt_time_total / 10
            rt_mae[i] = rt_mae_total / 10

    print("DT minimum MAE:", np.min(dt_mae))
    print("DT minimum MAE leaf size:", leaf_sizes[np.argmin(dt_mae)])
    print("RT minimum MAE:", np.min(rt_mae))
    print("RT minimum MAE leaf size:", leaf_sizes[np.argmin(rt_mae)])

    print("Average DT training time:", np.mean(dt_train_time))
    print("Average RT training time:", np.mean(rt_train_time))

    plt.figure()

    plt.plot(leaf_sizes, dt_mae, label="DTLearner MAE")
    plt.plot(leaf_sizes, rt_mae, label="RTLearner MAE")

    plt.xlabel("Leaf Size")
    plt.ylabel("Mean Absolute Error")
    plt.title("Experiment 3 - DT vs RT MAE")

    plt.legend()

    plt.savefig("./images/experiment3_mae.png")
    plt.close()

    plt.figure()

    plt.plot(leaf_sizes, dt_train_time, label="DTLearner Training Time")
    plt.plot(leaf_sizes, rt_train_time, label="RTLearner Training Time")

    plt.xlabel("Leaf Size")
    plt.ylabel("Training Time (seconds)")
    plt.title("Experiment 3 - DT vs RT Training Time")

    plt.legend()

    plt.savefig("./images/experiment3_time.png")
    plt.close()
