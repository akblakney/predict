# for analyzing market data as time series
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools  import   grangercausalitytests
from sklearn import preprocessing
import numpy as np
import json
import os
from utils import loadMarketForPlot, inRange, toReadableTime, loadTweetData, dateToUnix, marketFromID, parseArgs
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly.offline import iplot
import matplotlib.pyplot as plt
def loadMarketForTS(variable, marketDataPath, epochRange, marketID,cName):
    data = []
    setColumns = False
    columns = ['ds']
    for filename in os.listdir(marketDataPath):
        t = int(filename)
        if inRange(t,epochRange):
            f = open(marketDataPath + filename,'r')
            jsondata = f.read()
            jsondata = json.loads(jsondata)
        else:
            continue
        market = marketFromID(jsondata, marketID)
        contracts = market['contracts']
        prices = []
        prices.append(toReadableTime(t))
        for contract in contracts:
            if contract['name'] != cName:
                continue
            prices.append(contract['bestBuyYesCost'])
            if not setColumns:
                columns.append(contract['name'])
        setColumns = True
        data.append(prices)

    data = np.array(data)

    data = pd.DataFrame(data,columns=columns)
    return data

def tweetNearTime(d, tweets):
    t = dateToUnix(d)
    tweets = [dateToUnix(x) for x in tweets]
    for tweet in tweets:
        if abs(tweet - t) < 60:
            return 1
    return 0

def tweet_density(d, tweets):
    t = dateToUnix(d)
    # for testing
#    if t > 1577334400:
#        return np.exp(.0005 * -1) + np.exp(.0005 * -2)
    tweets = [dateToUnix(x) for x in tweets]
    density = 0
    N = 10000
    index = 0
    while index < len(tweets) and tweets[index] < t:
        if t - tweets[index] > N:
            index += 1
            continue
        density += np.exp(.0005 * (tweets[index] - t))
        index += 1

    return density

def addTweetsToDataFrame(tweets, data):
    tweets = [toReadableTime(x) for x in tweets]
    data['tweet'] = data['ds'].map(lambda x: tweet_density(x,tweets))
#    data['tweet'] = data['ds'].map(lambda x: tweetNearTime(x,tweets))
#    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#        print(data)
    return data


def var_try(data):
    steps = 60
    data2 = data[[cName,'tweet']]
    model = VAR(data2[[cName,'tweet']])
    results = model.fit(4)
    results.plot()
    model.select_order(15)
    results = model.fit(maxlags=15, ic = 'aic')
#    print('params')
#    print(results.params)
#    results.summary
#    results.plot()
    lag_order = results.k_ar
    print('abc')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(data2[cName])
    print('forecast here')
    print(results.forecast(data2.values[-lag_order:],60))

    results.plot_forecast(60)
     
def grangersCausality():
    # grangers causality
    #print('causality start')
    #print(grangercausalitytests(data[[cName, 'tweet']], maxlag=15, addconst=True, verbose=False))
    #print('causality end')
    return None

def prophetStuff():
    return None
    # prophet prediction stuff
    #data['cap'] = 1.0
    #data = data.rename(columns={cName : 'y'})
    #print('hhh')
#   print(data)

    #model = Prophet( growth='logistic')
    #model.add_regressor('tweet')
    #model.fit(data)
    #future = model.make_future_dataframe(periods=1)
    #future['cap'] = 1.0
    #future['tweet'] = future['ds'].apply(tweet)
    #forecast = model.predict(future)


    #fig1 = plot_plotly(model,forecast)
    #fig1.show()


#py.init_notebook_mode()

marketID, marketDataPath, tweetDataPath, plotType, epochRange = parseArgs()
cName = '555 or more'
#epochRange = [1577163600,15771755990]
data = loadMarketForTS('yes',marketDataPath, epochRange,marketID, cName)
tweets = loadTweetData(tweetDataPath, epochRange)
data = addTweetsToDataFrame(tweets, data)

# normalize and sort
x = data.tweet.values #returns a numpy array
m = np.amax(x)
x = [xx / m for xx in x]
data.tweet = x
data[cName] = data[cName].astype(float)

data = data.sort_values(by='ds')

var_try(data)


# plot data
data.plot(x='ds',y=['tweet', cName], title='original market data')


plt.show()



