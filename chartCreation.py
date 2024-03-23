from yahoo_fin.stock_info import *
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import requests
#alpha vantage api key: 7W2ZIAQCJJ70TTO3
    #TODO edit this to take in company name as argument along with requested data, run through NLP, output data and a chart

#index=pd.date_range("2021-11-10", periods=7, freq="d")) 
#Important keys

def createChart(company, startDate, endDate, interval='1d'):
    #This is UTC
    stock = get_data(company, start_date=startDate, end_date = endDate, interval=interval)
    #freq, T for min, H, D, M, Y
    interval = interval.replace('m', 'T').upper()
    #This is EST
    print(f"Interval: {interval}")
    dateRange = pd.date_range(startDate, endDate, freq=interval)
    dates = []
    for date in dateRange:
        dates.append(date)
    print(f"Length: {len(dates)}")

    print(stock)
    stock.insert(0, 'date', dates) 
    print(stock)
    print(stock.keys())

    ohlc = stock.loc[:, ['open', 'high', 'low', 'close']]
    ohlc.set_index(dateRange)
    mpf.plot(ohlc, type='candle', style='charles')

    print(ohlc)

    plt.figure(figsize=(17, 10))
    fig, ax = plt.subplots()

    #plt.plot(dates, stock['high'])
    fig.tight_layout()
    plt.grid(True)


if __name__ == '__main__':
    
    #use UTC because yahoo finance is cringe
    startDate = "03/18/2024 13:30:00"
    endDate = "03/18/2024 19:59:01"

    createChart('aapl', startDate, endDate, interval='1m')
