import os

import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir='../../data/'):
    """return csv file path given symbol"""
    return os.path.join(base_dir, '{}.csv'.format(str(symbol)))

def get_data(symbols, dates):
    """read adj close from given symbols csv file"""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True,
                              usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':
            df = df.dropna()

    return df

def plot_data(df,title="Stock Prices"):
    """plot stock prices"""
    ax = df.plot(title=title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()


def test_run():
    # define date range
    start_date='2010-01-01'
    end_date='2010-12-31'
    dates = pd.date_range(start_date, end_date)

    symbols = ['GOOG','IBM','GLD']
    df1 = get_data(symbols, dates)
    # print (df1['2010-01-01':'2010-01-31'])
    # print (df1[['GOOG','IBM']])
    plot_data(df1)

if __name__ == '__main__':
    test_run()