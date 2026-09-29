""""""  		  	   		 		  		  		  		    	 		 		   		 		  
"""MC1-P2: Optimize a portfolio.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
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
  		  	   		 		  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		  	   		 		  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 		  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  
from scipy.optimize import minimize	

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
    return "none"
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
# This is the function that will be tested by the autograder  		  	   		 		  		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		  	   		 		  		  		  		    	 		 		   		 		  
def optimize_portfolio(  		  	   		 		  		  		  		    	 		 		   		 		  
    sd=dt.datetime(2008, 1, 1),  		  	   		 		  		  		  		    	 		 		   		 		  
    ed=dt.datetime(2009, 1, 1),  		  	   		 		  		  		  		    	 		 		   		 		  
    syms=["GOOG", "AAPL", "GLD", "XOM"],  		  	   		 		  		  		  		    	 		 		   		 		  
    gen_plot=False,  		  	   		 		  		  		  		    	 		 		   		 		  
):  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		 		  		  		  		    	 		 		   		 		  
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		 		  		  		  		    	 		 		   		 		  
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		 		  		  		  		    	 		 		   		 		  
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		 		  		  		  		    	 		 		   		 		  
    statistics.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		 		  		  		  		    	 		 		   		 		  
    :type sd: datetime  		  	   		 		  		  		  		    	 		 		   		 		  
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		 		  		  		  		    	 		 		   		 		  
    :type ed: datetime  		  	   		 		  		  		  		    	 		 		   		 		  
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		 		  		  		  		    	 		 		   		 		  
        symbol in the data directory)  		  	   		 		  		  		  		    	 		 		   		 		  
    :type syms: list  		  	   		 		  		  		  		    	 		 		   		 		  
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		 		  		  		  		    	 		 		   		 		  
        code with gen_plot = False.  		  	   		 		  		  		  		    	 		 		   		 		  
    :type gen_plot: bool  		  	   		 		  		  		  		    	 		 		   		 		  
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		 		  		  		  		    	 		 		   		 		  
        standard deviation of daily returns, and Sharpe ratio  		  	   		 		  		  		  		    	 		 		   		 		  
    :rtype: tuple  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		  	   		 		  		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		  	   		 		  		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		  	   		 		  		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		  	   		 		  		  		  		    	 		 		   		 		  
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later  

    

    # find the allocations for the optimal portfolio  		  	   		 	 		  	   		 		  		  		  		    	 		 		   		 		  
    initial_allocs = np.ones(len(syms)) / len(syms)
    bounds = tuple((0.0, 1.0) for _ in range(len(syms))) 
    constraints = ({ 'type': 'eq', 'fun': lambda allocs: 1.0 - np.sum(allocs) })  

    maximized_allocs = minimize(maximize_sharpe_ratio, initial_allocs, args=(prices,), method='SLSQP', bounds=bounds, constraints=constraints).x

    normed = prices / prices.iloc[0]
    normed_SPY = prices_SPY / prices_SPY.iloc[0]
    alloced = normed * maximized_allocs 
    port_val = alloced.sum(axis=1)		  	   		 		  		  		  		    	 		 		   		 		

    daily_returns = get_daily_returns(port_val)
    cr = get_cumulative_return(port_val)
    adr = get_average_daily_return(daily_returns)
    sddr = get_std_dev_daily_returns(daily_returns)
    sr = get_sharpe_ratio(adr, sddr) 		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # Compare daily portfolio value with SPY using a normalized plot  		  	   		 		  		  		  		    	 		 		   		 		  
    if gen_plot:  		  	   		 		  		  		  		    	 		 		   		 		  
        # add code to plot here  		  	   		 		  		  		  		    	 		 		   		 		  
        df_temp = pd.concat(  		  	   		 		  		  		  		    	 		 		   		 		  
            [port_val, normed_SPY], keys=["Portfolio", "SPY"], axis=1  		  	   		 		  		  		  		    	 		 		   		 		  
        )  		  	   		 		  		  		  		    	 		 		   		 		  

        plt.plot(df_temp.index, df_temp["Portfolio"], label="Portfolio")
        plt.plot(df_temp.index, df_temp["SPY"], label="SPY")
        plt.xlabel("Date")
        plt.ylabel("Normalized Value")
        plt.title("Optimized Portfolio vs SPY")
        plt.legend()
        plt.savefig("./images/Figure1.png")
        plt.close()  # Save the plot as a PNG file 		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    return maximized_allocs, cr, adr, sddr, sr

def get_daily_returns(port_val):
    daily_returns = port_val.copy()
    daily_returns.iloc[1:] = (port_val.iloc[1:].values / port_val.iloc[:-1].values) - 1
    daily_returns.iloc[0] = 0.0
    return daily_returns  	

def get_cumulative_return(port_val):
    cumulative_return = (port_val.iloc[-1] / port_val.iloc[0]) - 1
    return cumulative_return

def get_average_daily_return(daily_returns):
    average_daily_return = daily_returns.iloc[1:].mean()
    return average_daily_return

def get_std_dev_daily_returns(daily_returns):
    std_dev_daily_returns = daily_returns.iloc[1:].std()
    return std_dev_daily_returns

def get_sharpe_ratio(average_daily_return, std_dev_daily_returns, daily_rf=0.0, k=252):
    sharpe_ratio = np.sqrt(k) * (average_daily_return - daily_rf) / std_dev_daily_returns
    return sharpe_ratio

def maximize_sharpe_ratio(allocs, prices):
    normed = prices / prices.iloc[0]
    alloced = normed * allocs 
    port_val = alloced.sum(axis=1)		  	   		 		  		  		  		    	 		 		   		 		

    daily_returns = get_daily_returns(port_val)
    adr = get_average_daily_return(daily_returns)
    sddr = get_std_dev_daily_returns(daily_returns)
    sr = get_sharpe_ratio(adr, sddr)
    return -sr	  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
def test_code():  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    This function WILL NOT be called by the auto grader.  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008, 6, 1)  		  	   		 		  		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2009, 6, 1)  		  	   		 		  		  		  		    	 		 		   		 		  
    symbols = ["IBM", "X", "GLD", "JPM"]  		  	   		 		  		  		  		    	 		 		   		 		
  		  	   		 		  		  		  		    	 		 		   		 		  
    # Assess the portfolio  		  	   		 		  		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		 		  		  		  		    	 		 		   		 		  
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True 		  	   		 		  		  		  		    	 		 		   		 		  
    )  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # Print statistics  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Start Date: {start_date}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"End Date: {end_date}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Symbols: {symbols}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Allocations:{allocations}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio: {sr}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Average Daily Return: {adr}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Cumulative Return: {cr}")  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		  	   		 		  		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		  	   		 		  		  		  		    	 		 		   		 		  
    test_code()  		  	   		 		  		  		  		    	 		 		   		 		  
