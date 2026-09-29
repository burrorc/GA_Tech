"""Analyze a portfolio.  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
Copyright 2017, Georgia Tech Research Corporation  		  	   		 		  		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332-0415  		  	   		 		  		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 		  		  		  		    	 		 		   		 		  
"""  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 		  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
# This is the function that will be tested by the autograder  		  	   		 		  		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		  	   		 		  		  		  		    	 		 		   		 		  
def assess_portfolio(
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 1, 1),
    syms=["GOOG", "AAPL", "GLD", "XOM"],
    allocs=[0.1, 0.2, 0.3, 0.4],
    sv=1000000,
    rfr=0.0,
    sf=252.0,
    gen_plot=False,
):
    """Compute portfolio metrics for a given asset mix over a date range."""
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]
    prices_SPY = prices_all["SPY"]

    allocs = np.asarray(allocs, dtype=float)
    if np.isclose(allocs.sum(), 0.0):
        raise ValueError("Allocations must sum to a non-zero value.")
    allocs = allocs / np.sum(allocs)

    normed = prices / prices.iloc[0]
    alloced = normed * allocs
    port_val = alloced.sum(axis=1) * sv

    daily_rets = port_val.pct_change().dropna()
    cr = port_val.iloc[-1] / port_val.iloc[0] - 1.0
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = 0.0 if sddr == 0 else ((adr - rfr) / sddr) * np.sqrt(sf)

    if gen_plot:
        df_temp = pd.concat(
            [port_val / port_val.iloc[0], prices_SPY / prices_SPY.iloc[0]],
            keys=["Portfolio", "SPY"],
            axis=1,
        )
        plot_data(df_temp, title="Normalized Portfolio Value", ylabel="Normalized Price")

    ev = port_val.iloc[-1]
    return cr, adr, sddr, sr, ev  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
def test_code():  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    Performs a test of your code and prints the results  		  	   		 		  		  		  		    	 		 		   		 		  
    """  		  	   		 		  		  		  		    	 		 		   		 		  
    # This code WILL NOT be tested by the auto grader  		  	   		 		  		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # Define input parameters  		  	   		 		  		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		  	   		 		  		  		  		    	 		 		   		 		  
    # the autograder!  		  	   		 		  		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2009, 1, 1)  		  	   		 		  		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2010, 1, 1)  		  	   		 		  		  		  		    	 		 		   		 		  
    symbols = ["GOOG", "AAPL", "GLD", "XOM"]  		  	   		 		  		  		  		    	 		 		   		 		  
    allocations = [0.2, 0.3, 0.4, 0.1]  		  	   		 		  		  		  		    	 		 		   		 		  
    start_val = 1000000  		  	   		 		  		  		  		    	 		 		   		 		  
    risk_free_rate = 0.0  		  	   		 		  		  		  		    	 		 		   		 		  
    sample_freq = 252  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # Assess the portfolio  		  	   		 		  		  		  		    	 		 		   		 		  
    cr, adr, sddr, sr, ev = assess_portfolio(  		  	   		 		  		  		  		    	 		 		   		 		  
        sd=start_date,  		  	   		 		  		  		  		    	 		 		   		 		  
        ed=end_date,  		  	   		 		  		  		  		    	 		 		   		 		  
        syms=symbols,  		  	   		 		  		  		  		    	 		 		   		 		  
        allocs=allocations,  		  	   		 		  		  		  		    	 		 		   		 		  
        sv=start_val,  		  	   		 		  		  		  		    	 		 		   		 		  
        gen_plot=False,  		  	   		 		  		  		  		    	 		 		   		 		  
    )  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
    # Print statistics  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Start Date: {start_date}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"End Date: {end_date}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Symbols: {symbols}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Allocations: {allocations}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio: {sr}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Average Daily Return: {adr}")  		  	   		 		  		  		  		    	 		 		   		 		  
    print(f"Cumulative Return: {cr}")  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    test_code()  		  	   		 		  		  		  		    	 		 		   		 		  
