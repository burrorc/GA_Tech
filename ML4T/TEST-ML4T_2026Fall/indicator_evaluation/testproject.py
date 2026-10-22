	  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		 		  		  		  		    	 		 		   		 		  
import os  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 		  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  

import TheoreticallyOptimalStrategy as tos
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt


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

def get_portfolio_stats(portvals):
    values = portvals.iloc[:,0]
    cum_return = values.iloc[-1] / values.iloc[0] -1
    daily_returns = values.pct_change().dropna()
    return cum_return, daily_returns.std(), daily_returns.mean()


def get_tos():
    symbol = "JPM"
    sv = 100000
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)

    trades = tos.testPolicy(symbol, sd, ed, sv)
    tos_values = compute_portvals(trades, sv, 0.0, 0.0 )
    tos_stats = get_portfolio_stats(tos_values)

    bmark_trades = pd.DataFrame(0, index=trades.index, columns=[symbol])
    bmark_trades.iloc[0,0] = 1000

    bmark_values = compute_portvals(bmark_trades, sv, 0.0, 0.0)
    bmark_stats = get_portfolio_stats(bmark_values)

    with open("p6_results.txt", "w") as file:
        file.write(f"{'Metric':<25} {'Benchmark':>15} {'TOS':>15}\n")
        file.write(f"{'Cumulative Return':<25} {bmark_stats[0]:>15.6f} {tos_stats[0]:>15.6f}\n")
        file.write(f"{'Std Daily Return':<25} {bmark_stats[1]:>15.6f} {tos_stats[1]:>15.6f}\n")
        file.write(f"{'Mean Daily Return':<25} {bmark_stats[2]:>15.6f} {tos_stats[2]:>15.6f}\n")

    normalized_bmark = bmark_values / bmark_values.iloc[0, 0]
    normalized_tos = tos_values / tos_values.iloc[0, 0]

    plt.figure(figsize=(12,8))
    plt.plot(normalized_bmark.index, normalized_bmark.iloc[:,0], color="purple", label="Benchmark")
    plt.plot(normalized_tos.index, normalized_tos.iloc[:,0], color="red", label="TOS")

    plt.title("Theoretically Optimal Strategy vs. Benchmark - JPM")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (Normalized)")
    plt.legend()
    plt.grid(True)

    plt.savefig("tos_comparison.png", bbox_inches="tight")
    plt.close()

  		  	   		 		  		  		  		    	 		 		   		 		  
		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    get_tos()  		  	   		 		  		  		  		    	 		 		   		 		  
