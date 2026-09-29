import numpy as np  		  	   		 		  		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import BagLearner as bl  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
class InsaneLearner(object): 		  	   		 		  		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False):	  	   		 		  		  		  		    	 		 		   		 		  
        self.verbose = verbose
        self.learners = [bl.BagLearner(lrl.LinRegLearner, {}, 20, False, self.verbose) for i in range(20)]

    def add_evidence(self, data_x, data_y):
        for learner in self.learners:
            learner.add_evidence(data_x, data_y)

    def author(self):
        return "rburrows3"
  		  	   		 		  		  		  		    	 		 		   		 		  
    def query(self, points):
        predicted_values = [learner.query(points) for learner in self.learners]
        return np.mean(predicted_values, axis=0)
		  	   		 		  		  		  		    	 		 		   		 		  
