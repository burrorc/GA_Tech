	  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		 		  		  		  		    	 		 		   		 		  
import os  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 		  		  		  		    	 		 		   		 		  
from util import get_data, plot_data  

import TheoreticallyOptimalStrategy as tos
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
from indicators import price_over_sma,bollinger_b,momentum, macd_histo, cci


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

    plt.title("JPM: Theoretically Optimal Strategy vs. Benchmark")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (Normalized)")
    plt.legend()
    plt.grid(True)

    plt.savefig("tos_comparison.png", bbox_inches="tight")
    plt.close()

def get_indicators():
    symbol = "JPM"
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)

    backfill_date = sd - dt.timedelta(days=60)
    dates = pd.date_range(backfill_date, ed)

    prices = get_data([symbol], dates)[symbol]

    # SMA RATIO

    sma = prices.rolling(window=20).mean()
    sma_ratio = price_over_sma(prices, window=20)

    results = pd.DataFrame({ "Price": prices, "SMA_20": sma,"Price_SMA": sma_ratio})

    results = results.loc[sd:ed]

    normalized_price = results["Price"] / results["Price"].iloc[0]
    normalized_sma = results["SMA_20"] / results["Price"].iloc[0]

    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(12, 8),sharex=True)

    ax1.plot(results.index, normalized_price, label="JPM Price")
    ax1.plot(results.index, normalized_sma, label="20-Day SMA")
    ax1.set_title("JPM: Price/SMA (20 Day)")
    ax1.set_ylabel("Normalized Price")
    ax1.legend()
    ax1.grid(True)

    ax2.plot(results.index, results["Price_SMA"], color="green", label="Price/SMA Ratio")
    ax2.axhline(1.0, color="gray", linestyle="--", label="Ratio = 1.0")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Price/SMA Ratio")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("sma_indicator.png")
    plt.close()

    # BOLLINGER %B

    percent_b = bollinger_b(prices)

    sma = prices.rolling(window=20).mean()
    std = prices.rolling(window=20).std()

    upper_band = sma + 2 * std
    lower_band = sma - 2 * std

    bb_results = pd.DataFrame({ "Price": prices,"SMA": sma,"Upper": upper_band,"Lower": lower_band,"Percent_B": percent_b }).loc[sd:ed]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.plot(bb_results.index, bb_results["Price"], label="JPM Price")
    ax1.fill_between( bb_results.index,bb_results["Lower"],bb_results["Upper"],alpha=0.2,label="Bollinger Band Range")

    ax1.set_title("JPM: Bollinger Bands %B (20 Day, 2 Std Dev)")
    ax1.set_ylabel("Price ($)")
    ax1.legend()
    ax1.grid(True)

    ax2.plot(bb_results.index, bb_results["Percent_B"], color="green", label="Bollinger %B")
    ax2.axhline(1.0, color="red", linestyle="--", label="Upper Band (1.0)")
    ax2.axhline(0.0, color="blue", linestyle="--", label="Lower Band (0.0)")
    ax2.axhline(0.5, color="gray", linestyle=":", label="Middle Band (0.5)")

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Bollinger %B")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("bollinger_b_indicator.png")
    plt.close()

    # MOMENTUM
    momentum_values = momentum(prices, window=10)

    momentum_results = pd.DataFrame({ "Price": prices, "Price_10_Days_Ago": prices.shift(10), "Momentum": momentum_values}).loc[sd:ed]

    normalized_price = momentum_results["Price"] / momentum_results["Price"].iloc[0]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.plot( momentum_results.index,normalized_price, label="JPM Price")
    ax1.set_title("JPM: Momentum (10 day)")
    ax1.set_ylabel("Normalized Price")
    ax1.legend()
    ax1.grid(True)

    ax2.bar( momentum_results.index,momentum_results["Momentum"],color=[
            "green" if value >= 0 else "red"
            for value in momentum_results["Momentum"]
        ],width=2)

    ax2.axhline(0, color="gray", linestyle="--")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("10-Day Momentum")

    plt.tight_layout()
    plt.savefig("momentum_indicator.png")
    plt.close()

    # MACD HISTO
    macd_values = macd_histo(prices)

    small_ema = prices.ewm(span=12, adjust=False).mean()
    large_ema = prices.ewm(span=26, adjust=False).mean()

    macd_line = small_ema - large_ema
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    macd_chart = pd.DataFrame({ "MACD": macd_line,"Signal": signal_line,"Histogram": macd_values}).loc[sd:ed]

    fig, (ax1, ax2) = plt.subplots( 2, 1, figsize=(12, 8), sharex=True)

    ax1.plot(macd_chart.index, macd_chart["MACD"], label="MACD")
    ax1.plot(macd_chart.index, macd_chart["Signal"], label="Signal Line")
    ax1.axhline(0, color="gray", linestyle="--")
    ax1.set_title("JPM: MACD Histogram (12, 26, 9)")
    ax1.set_ylabel("MACD")
    ax1.legend()
    ax1.grid(True)

    ax2.bar( macd_chart.index,macd_chart["Histogram"],color=[
            "green" if value >= 0 else "red"
            for value in macd_chart["Histogram"]],width=2)

    ax2.axhline(0, color="gray", linestyle="--")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("MACD Histogram")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("macd_histo_indicator.png")
    plt.close()

    # CCI

    high = get_data([symbol], dates, colname="High")[symbol]
    low = get_data([symbol], dates, colname="Low")[symbol]
    close = get_data([symbol], dates, colname="Close")[symbol]

    cci_values = cci(high, low, close, window=20)

    cci_results = pd.DataFrame({ "Close": close,"CCI": cci_values}).loc[sd:ed]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.plot(cci_results.index, cci_results["Close"], label="JPM Closing Price")
    ax1.set_title("JPM: CCI (20 Day)")
    ax1.set_ylabel("Closing Price ($)")
    ax1.legend()
    ax1.grid(True)

    ax2.plot(cci_results.index, cci_results["CCI"], color="purple", label="CCI")
    ax2.axhline(100, color="green", linestyle="--", label="+100")
    ax2.axhline(-100, color="red", linestyle="--", label="-100")
    ax2.axhline(0, color="gray", linestyle=":", label="Zero")

    ax2.set_xlabel("Date")
    ax2.set_ylabel("CCI")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("cci_indicator.png")
    plt.close()


  		  	   		 		  		  		  		    	 		 		   		 		  
		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
  		  	   		 		  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 		  		  		  		    	 		 		   		 		  
    get_tos()
    get_indicators()  		  	   		 		  		  		  		    	 		 		   		 		  
