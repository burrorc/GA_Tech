""""""  		  	   		 		  		  		  		    	 		 		   		 		  
"""  		  	   		 		  		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
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
  		  	   		 		  		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		 		  		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		 		  		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		 		  		  		  		    	 		 		   		 		  
"""  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import datetime as dt 	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import pandas as pd  
import RTLearner as rt
import BagLearner as bl	
import indicators as ind	
import numpy as np  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		 		  		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		 		  		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		 		  		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		 		  		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		 		  		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		 		  		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    # constructor  		  	   		 		  		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        Constructor method  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		 		  		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		 		  		  		  		    	 		 		   		 		  
        self.commission = commission 
        self.peek = 3
        self.leaf_size = 20
        self.bags = 100
        self.vol_window = 20
        self.vol_multiplier = 0.35
        self.learner = bl.BagLearner(learner=rt.RTLearner,kwargs={"leaf_size": self.leaf_size},
            bags=self.bags,boost=False,verbose=self.verbose)

    def author(self):
        return "rburrows3"

    def study_group(self):
        return "rburrows3"

    def get_labels(self, prices):

        future_prices = prices.shift(-self.peek)
        future_returns = future_prices/prices - 1

        commission_fee = (2 * self.commission / (1000 * prices))

        volatility = (prices.pct_change().rolling(window=self.vol_window).std().shift(1))


        base_threshold = (self.vol_multiplier * volatility * np.sqrt(self.peek))


        threshold = (base_threshold + 2 * self.impact + commission_fee)

        labels = pd.Series(0, index=prices.index)
        labels.loc[future_returns > threshold] = 1
        labels.loc[future_returns < -threshold] = -1

        valid = (future_returns.notna() & pd.notna(threshold))

        labels = labels.where(valid)

        return labels   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		  	   		 		  		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		 		  		  		  		    	 		 		   		 		  
        self,  		  	   		 		  		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		 		  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		 		  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		 		  		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		 		  		  		  		    	 		 		   		 		  
    ):  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		 		  		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		 		  		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		 		  		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		 		  		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		 		  		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		 		  		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		 		  		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
        # add your code to do learning here
        # 

        prices, features = ind.get_features(symbol, sd, ed)

        labels = self.get_labels(prices)

        valid_labels = (features.notna().all(axis=1) & labels.notna())

        data_x = features.loc[valid_labels].to_numpy()
        data_y = labels.loc[valid_labels].to_numpy()

        if (self.verbose):
            print("Training X:", data_x.shape)
            print("Training Y:", data_y.shape)
            print("Training classes:", np.unique(data_y))


        self.learner.add_evidence(data_x, data_y)
	  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		 		  		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		 		  		  		  		    	 		 		   		 		  
        self,  		  	   		 		  		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		 		  		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		 		  		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		 		  		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		 		  		  		  		    	 		 		   		 		  
    ):  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		 		  		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		 		  		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		 		  		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		 		  		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		 		  		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		 		  		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		 		  		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		 		  		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		 		  		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		 		  		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		 		  		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		 		  		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		 		  		  		  		    	 		 		   		 		  
        """  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
        # here we build a fake set of trades  		  	   		 		  		  		  		    	 		 		   		 		  
        # your code should return the same sort of data  		  	   		 		  		  		  		    	 		 		   		 		  
        # dates = pd.date_range(sd, ed)  		  	   		 		  		  		  		    	 		 		   		 		  
        # prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades = prices_all[[symbol,]]  # only portfolio symbols  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades.values[:, :] = 0  # set them all to nothing  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades.values[0, :] = 1000  # add a BUY at the start  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades.values[40, :] = -1000  # add a SELL  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades.values[41, :] = 1000  # add a BUY  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades.values[60, :] = -2000  # go short from long  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades.values[61, :] = 2000  # go long from short  		  	   		 		  		  		  		    	 		 		   		 		  
        # trades.values[-1, :] = -1000  # exit on the last day  		  	   		 		  		  		  		    	 		 		   		 		  
        # if self.verbose:  		  	   		 		  		  		  		    	 		 		   		 		  
        #     print(type(trades))  # it better be a DataFrame!  		  	   		 		  		  		  		    	 		 		   		 		  
        # if self.verbose:  		  	   		 		  		  		  		    	 		 		   		 		  
        #     print(trades)  		  	   		 		  		  		  		    	 		 		   		 		  
        # if self.verbose:  		  	   		 		  		  		  		    	 		 		   		 		  
        #     print(prices_all)  
        # 

        prices, features = ind.get_features(symbol, sd, ed)
        valid = features.notna().all(axis=1)

        signals = pd.Series(0, index=features.index)

        if(valid.any()):
            data_x = features.loc[valid].to_numpy()

            predictions = self.learner.query(data_x)
            signals.loc[valid] = predictions

    

        trades = ind.convert_to_trades(signals, symbol)		  	   		 		  		  		  		    	 		 		   		 		  
        return trades  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		 		  		  		  		    	 		 		   		 		  
