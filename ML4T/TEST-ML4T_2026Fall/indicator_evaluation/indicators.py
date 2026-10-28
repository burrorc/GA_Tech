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
    return "rburrows3"  # replace tb34 with your Georgia Tech username.	  	   		 		  		  		  		    	 		 		   		 		  
                                                                                              
def study_group():
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: The study group  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 		  		  		  		    	 		 		   		 
    """
    return "rburrows3"# Change this to your user ID  		

def price_over_sma(prices, window=20):
    sma = prices.rolling(window).mean()
    results = prices/sma
    return results

def bollinger_b(prices, window=20, factor_std=2):
    sma = prices.rolling(window).mean()
    std = prices.rolling(window).std()

    upper = sma + factor_std * std
    lower = sma - factor_std * std

    results = (prices - lower)/(upper-lower)

    return results

def momentum(prices, window=10):
    results = prices/prices.shift(window) -1

    return results

def macd_histo(prices, small=12, large=26, sig=9):
    small_ema = prices.ewm(span=small, adjust=False).mean()
    large_ema = prices.ewm(span=large, adjust=False).mean()

    macd = small_ema - large_ema

    sig_line = macd.ewm(span=sig, adjust=False).mean()

    results = macd - sig_line

    return results

def cci(high, low, close, window=20):
    typical_price = (high + low + close)/3

    typical_sma = typical_price.rolling(window).mean()

    mean_dev = typical_price.rolling(window).apply(lambda x: abs(x-x.mean()).mean())

    results = (typical_price - typical_sma) / (0.015 * mean_dev)
    return results
