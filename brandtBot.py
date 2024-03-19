import yfinance as yf
from yahoo_fin.stock_info import *
from yahoo_fin.options import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf


#index=pd.date_range("2021-11-10", periods=7, freq="d")) 
#Important keys
startDate = "03/18/2024 09:30:00"
endDate = "03/18/2024 15:59:00"

aapl = get_data("aapl", start_date=startDate, end_date = "03/18/2024 20:00:00", interval="1m")
dateRange = pd.date_range(startDate, endDate, freq='T')
dates = []
for date in dateRange:
    dates.append(date)
print(f"Length: {len(dates)}")

print(aapl)
aapl.insert(0, 'date', dates) 
print(aapl)
print(aapl.keys())

ohlc = aapl.loc[:, ['open', 'high', 'low', 'close']]
mpf.plot(ohlc, type='candle', style='charles')

print(ohlc)

plt.figure(figsize=(17, 10))
fig, ax = plt.subplots()


'''
plt.plot(dates, aapl['high'])
plt.plot(dates, aapl['low'])
plt.plot(dates, aapl['open'])
plt.plot(dates, aapl['close'])
'''
fig.tight_layout()
plt.grid(True)

