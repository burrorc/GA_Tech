""""""  		  	   		 		  		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
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
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
def compute_portvals(  		  	   		 		  		  		  		    	 		 		   		 		  
    trades_df,  		  	   		 		  		  		  		    	 		 		   		 		  
    start_val=100000,  		  	   		 		  		  		  		    	 		 		   		 		  
    commission=0.00,  		  	   		 		  		  		  		    	 		 		   		 		  
    impact=0.00,  		  	   		 		  		  		  		    	 		 		   		 		  
):  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		 		  		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		 		  		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		 		  		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		 		  		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 		  		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		 		  		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 		  		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		  	   		 		  		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		 		  		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		  	   		 		  		  		  		    	 		 		   		 		  
    # TODO: Your code here  	
    # 

    trades_df = trades_df.sort_index()

    start_date = trades_df.index.min()
    end_date = trades_df.index.max()
    period_dates = pd.date_range(start_date, end_date)

    symbols = list(trades_df.columns)
    prices = get_data(symbols, period_dates)
    prices = prices[symbols]

    trades = pd.DataFrame(0.0, index=prices.index, columns=list(symbols) + [
        "NetCash",
        "NumTrades",
        "CommissionCosts",
        "ImpactCosts"])

    for date in trades_df.index:
        for symbol in symbols:
            shares = trades_df.loc[date,symbol]
            if shares == 0:
                continue

            exec_price = prices.loc[date,symbol]
            impact_cost = abs(shares) * exec_price * impact
            cash_change = shares * exec_price

            trades.loc[date, symbol] += shares
            trades.loc[date, "NumTrades"] += 1
            trades.loc[date, "CommissionCosts"] += commission
            trades.loc[date, "ImpactCosts"] += impact_cost
            trades.loc[date, "NetCash"] -= cash_change + (commission + impact_cost)

        
    portfolio = trades[list(symbols) + ["NetCash"]].cumsum()
    portfolio["NetCash"] += start_val

    stock_values = portfolio[list(symbols)] * prices
    portvals = stock_values.sum(axis=1) + portfolio["NetCash"]

    portvals_df = portvals.to_frame(name= "Portfolio Value")

    return portvals_df		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
 	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    pass		  	   		 		  		  		  		    	 		 		   		 		  
