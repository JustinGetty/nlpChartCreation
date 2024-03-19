import yfinance as yf
from yahoo_fin.stock_info import *
from yahoo_fin.options import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Important keys
startDate = "03/18/2024 09:30:00"
endDate = "03/18/2024 15:59:00"

aapl = get_data("aapl", start_date=startDate, interval="1m")
dateRange = pd.date_range(startDate, endDate, freq='T')
dates = []
for date in dateRange:
    dates.append(date)
print(f"Length: {len(dates)}")

aapl.insert(0, 'date', dates) 

print(aapl)
print(aapl.keys())


plt.plot(dates, aapl['high'])
plt.plot(dates, aapl['low'])
plt.grid(True)
plt.show()
