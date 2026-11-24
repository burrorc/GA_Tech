import datetime as dt
import pandas as pd
import indicators as ind


class ManualStrategy:

    def __init__(self, verbose=False, impact =0.0, commission =0.0):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.bb_threshold = 0.1
        self.macd_threshold = 0.05
        self.mom_threshold = 0.0

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
        return "rburrows3"# Change this to your user ID  


    def get_signs(self, features):

        signs = pd.DataFrame(index=features.index)

        signs["BB"] = 0
        signs.loc[features["BB"] < self.bb_threshold, "BB"] = 1
        signs.loc[features["BB"] > (1-self.bb_threshold), "BB"] = -1


        signs["MACD"] = 0
        signs.loc[features["MACD"] < -self.macd_threshold, "MACD"] = 1
        signs.loc[features["MACD"] > self.macd_threshold, "MACD" ] = -1

        signs["MOM"] = 0
        signs.loc[features["MOM"] < -self.mom_threshold, "MOM"] = 1
        signs.loc[features["MOM"] > self.mom_threshold, "MOM"] = -1

        return signs


    def testPolicy(self, symbol="IBM",
                   sd=dt.datetime(2008, 1, 1),
                   ed=dt.datetime(2009, 1, 1),
                   sv=100000):

        prices, features = ind.get_features(symbol, sd, ed)

        signs = self.get_signs(features)
        scores = signs.sum(axis=1)

        signals = pd.Series(0, index=features.index)

        current_position = 0

        for i in range(len(scores)):

            if not features.iloc[i].isna().any():

                if scores.iloc[i] >= 2:
                    current_position = 1

                elif scores.iloc[i] <= -2:
                    current_position = -1

            signals.iloc[i] = current_position

        return ind.convert_to_trades(signals, symbol)

   