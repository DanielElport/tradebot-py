from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt  # For datetime objects
from dateutil.relativedelta import relativedelta
import pandas_datareader.data as web
from strategies.MaCrossMultiple import MaCrossMultiple
from strategies.TrendFollowing import ClenowTrendFollowingStrategy

# Import the backtrader platform
import backtrader as bt

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    stocks = ['AAPL']

    start = dt.datetime.now() - relativedelta(years=2)
    end = dt.datetime.now() - relativedelta(years=0)

    for s in stocks:
        df = web.DataReader(s, "yahoo", start, end)
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data, name=s)

    INITIAL_CASH = 10000
    cerebro.broker.setcash(INITIAL_CASH)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    cerebro.broker.setcommission(commission=0.001)

    # Add a strategy
    cerebro.optstrategy(MaCrossMultiple, fast=range(10, 30), slow=range(30, 100))

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)
    cerebro.broker.setcommission(commission=0.001)

    # Run over everything
    cerebro.run(maxcpus=4)
