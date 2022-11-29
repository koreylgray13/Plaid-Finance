import pandas_datareader as web
import datetime as dt

from_date = '2021-08-01'
to_date = dt.datetime.now()
xrp = web.DataReader('XRP-USD', 'yahoo', from_date, to_date)
