""""""  		  	   		 		  		  		  		    	 		 		   		 		  
"""  		  	   		 		  		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
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
  		  	   		 		  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
class RTLearner(object):  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    This is a Random Tree Learner. It is implemented correctly.  		  	   		 		  		  		  		    	 		 		   		 		
  		  	   		 		  		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		 		  		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		 		  		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size=1, verbose=False):  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        Constructor method  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        self.leaf_size = leaf_size
        self.verbose = verbose  # move along, these aren't the drones you're looking for  
        self.tree = None  
  		  	   		 		  		  		  		    	 		 		   		 		  
    def author(self):
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        :return: The GT username of the student  		  	   		 		  		  		  		    	 		 		   		 		  
        :rtype: str  		  	   		 		  		  		  		    	 		 		   		 		  
        """
        return "rburrows3"  # replace tb34 with your Georgia Tech username.	  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    def study_group(self):
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        :return: The study group  		  	   		 		  		  		  		    	 		 		   		 		  
        :rtype: str  		  	   		 		  		  		  		    	 		 		   		 
        """
        return "none"

    def add_evidence(self, data_x, data_y):  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
        :param data_x: A set of feature values used to train the learner  		  	   		 		  		  		  		    	 		 		   		 		  
        :type data_x: numpy.ndarray  		  	   		 		  		  		  		    	 		 		   		 		  
        :param data_y: The value we are attempting to predict given the X data  		  	   		 		  		  		  		    	 		 		   		 		  
        :type data_y: numpy.ndarray  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
        self.tree = self.build_tree(data_x, data_y)	   		 		  		  		  		    	 		 		   		 		
  		  	   		 		  		  		  		    	 		 		   		 		  
    def query(self, points):  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        Estimate a set of test points given the model we built.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		 		  		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		 		  		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		 		  		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		 		  		  		  		    	 		 		   		 		  
        """  	
        predicted_values = np.zeros(points.shape[0])

        for point in range(points.shape[0]):
            current_node = 0
            while self.tree[current_node, 0] != -1:
                feature = int(self.tree[current_node, 0])
                split_val = self.tree[current_node, 1]
                if points[point, feature] <= split_val:
                    current_node += int(self.tree[current_node, 2])
                else:
                    current_node += int(self.tree[current_node, 3])
            predicted_values[point] = self.tree[current_node, 1]

        return predicted_values

    def build_tree(self, data_x, data_y):
        if(data_x.shape[0] <= self.leaf_size): 
            return np.array([[-1, np.mean(data_y), np.nan, np.nan]])
        elif(np.all(data_y == data_y[0])):
            return np.array([[-1, data_y[0], np.nan, np.nan]])
        else:
            best_feature = np.random.randint(0, data_x.shape[1])
            split_val = np.median(data_x[:, best_feature])

            left_nodes = data_x[:, best_feature] <= split_val
            right_nodes = data_x[:, best_feature] > split_val

            if np.sum(left_nodes) == 0 or np.sum(right_nodes) == 0:
                return np.array([[-1, np.mean(data_y), np.nan, np.nan]])

            left_tree = self.build_tree(data_x[left_nodes], data_y[left_nodes])
            right_tree = self.build_tree(data_x[right_nodes], data_y[right_nodes])

            root_node = np.array([[best_feature, split_val, 1, left_tree.shape[0] + 1]])

            partial_tree = np.append(root_node, left_tree, axis=0)
            full_tree = np.append(partial_tree, right_tree, axis=0)
            return full_tree

  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    pass	  	   		 		  		  		  		    	 		 		   		 		  
