"""
Student Name: Robert Burrows (replace with your name)  		  	   		 		  		  		  		    	 		 		   		 		  
GT User ID: rburrows3 (replace with your User ID)  		  	   		 		  		  		  		    	 		 		   		 		  
GT ID: 904201091 (replace with your GT ID)  	 		  	   		 		  		  		  		    	 		 		   		 		  
"""  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		 		  		  		  		    	 		 		   		 		  
import os  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 		  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  

def author():
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 		  		  		  		    	 		 		   		 		  
    """
    return "rburrows3"

def study_group():
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: The study group  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 		  		  		  		    	 		 		   		 
    """
    return "rburrows3"# Change this to your user ID  		

def testPolicy(
        symbol="AAPL", 
        sd=dt.datetime(2010,1,1), 
        ed=dt.datetime(2011,12,31), 
        sv=100000):

    dates = pd.date_range(sd, ed)
    prices_df = get_data([symbol], dates)
    prices = prices_df[symbol]

    next_prices = prices.shift(-1)
    next_changes = next_prices - prices

    target_positions = pd.Series(float("nan"), index=prices.index)
    target_positions[next_changes > 0] = 1000
    target_positions[next_changes <0] = -1000

    target_positions =  target_positions.ffill().fillna(0).astype(int)

    trades = target_positions - target_positions.shift(1, fill_value=0)

    df_trades = trades.to_frame(name=symbol)

    return df_trades