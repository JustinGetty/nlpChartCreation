from yahoo_fin.stock_info import *
import re
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import spacy
import yahooquery as yq
#alpha vantage api key: 7W2ZIAQCJJ70TTO3

#TODO Make chart in EST (standardize date range and stock pull)
#TODO range should only be within trading hours for the pd.daterange

#index=pd.date_range("2021-11-10", periods=7, freq="d")) 
#Important keys
nlp = spacy.load("en_core_web_lg")

#sentence = 'The company Amazon from  03/03/2024 at 13:30 am to 03/05/2024 at the time 19:59 pm with 1 minute intervals'
sentence = input('Enter sentence below: ')

def stripText(word):
   word = re.sub(r"[a-zA-Z]", "", str(word))   
   return word

def pullEntities(sentence):
    doc = nlp(sentence)
    time, date, org = [], [], []
    for ent in doc.ents:        
        if ent.label_ == 'ORG':
            org.append(ent.text)
        elif ent.label_ == 'DATE':
            date.append(ent.text)
        elif ent.label_ == 'TIME':
            time.append(ent.text)
        #print(ent.text, ent.label_)
    if len(time) == 1:
        timeRaw = time[0]
        startTime = None
    elif len(time) > 1:
        startTime = stripText(time[0])
        endTime = stripText(time[1])
        timeRaw = time[2]
    company = org[0]  
    print(org)
    startDate = stripText(date[0])
    endDate = stripText(date[1])
    timeRaw = str(timeRaw).split()
    timeUnit = timeRaw[1].lower()
    if timeUnit not in ['minute', 'hour', 'day', 'week', 'month', 'year']:
        print("Error please input interval unit as non-plural unit spelled correctly")

    timeUnit = timeUnit[0]
    if timeUnit == 'w':
        timeUnit = 'wk'
    cringeTuple = (timeRaw[0], timeUnit)
    intervalFinal = "".join(cringeTuple)

    if startTime == None:
        return (company, startDate, endDate, intervalFinal)
    else:
        return (company, startDate, endDate, intervalFinal, startTime, endTime)

#symbol lookup stuff

def getSymbol(query, preferred_exchange='AMS'):
    try:
        data = yq.search(query)
    except ValueError: # Will catch JSONDecodeError
        print(query)
    else:
        quotes = data['quotes']
        if len(quotes) == 0:
            return 'No Symbol Found'

        symbol = quotes[0]['symbol']
        for quote in quotes:
            if quote['exchange'] == preferred_exchange:
                symbol = quote['symbol']
                break
        return symbol

#endDate = None?
def createChart(company, startDate, endDate, interval='1d', startTime = '13:30', endTime = '19:59'):
    #This is UTC
    startDate = (startDate, startTime)
    startDate = " ".join(startDate)
    endDate = (endDate, endTime)
    endDate = " ".join(endDate)
    try:
        #add minute parameters, pass minute as second argument, default to open/close, use join
        stock = get_data(company, start_date=startDate, end_date=endDate, interval=interval)
    except:
        print("error in stock retrieval")
    

    #freq, T for min, H, D, M, Y
    interval = interval.replace('m', 'T').upper()
    #This is EST
    dateRange = pd.date_range(startDate, endDate, freq=interval)
    dates = []
    for date in dateRange:
        dates.append(date)

    print(stock)

    try: 
        stock.insert(0, 'date', dates) 
    except:
        print("couldn't insert dates into the frame")
    print(stock)
    print(stock.keys())

    ohlc = stock.loc[:, ['open', 'high', 'low', 'close']]

    #fix this to have more precise range (i.e. minutes)
    #ohlc.set_index(dateRange)
    mpf.plot(ohlc, type='candle', style='charles')

    print(ohlc)

    plt.figure(figsize=(17, 10))
    fig, ax = plt.subplots()

    #plt.plot(dates, stock['high'])
    fig.tight_layout()
    plt.grid(True)


if __name__ == '__main__':
    
    print(f'Company: {getSymbol(pullEntities(sentence)[0])}\nStart Date: {pullEntities(sentence)[1]}\nEnd Date: {pullEntities(sentence)[2]}\nInterval: {pullEntities(sentence)[3]}')
    startDate = str(pullEntities(sentence)[1])
    endDate = str(pullEntities(sentence)[2])
    #company, startDate, endDate, interval, startTime, endTime    
    createChart(getSymbol(pullEntities(sentence)[0]).lower(), startDate, endDate, pullEntities(sentence)[3])  
