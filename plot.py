import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
from utils import loadTweetData, loadMarketForPlot, toReadableTime, parseArgs

# in epoch range for plotting?
def inRange(t):
    if epochRange is None:
        return True
    return t > epochRange[0] and t < epochRange[1]



def risk(market):
    risk = 0
    for contract in market['contracts']:
        if contract['bestBuyNoCost'] is None:
            continue
        risk += 1 - float(contract['bestBuyNoCost'])
    risk *= 100
    return risk

def plot(marketID, variable, tweets):
    marketdata, marketName = loadMarketForPlot(variable,marketDataPath,epochRange, marketID)
#    for t in marketdata:

    if variable == 'yes':
        varTitle = 'yes prices'
    if variable == 'no':
        varTitle = 'no prices'
    if variable == 'risk':
        varTitle = 'market risk'
    title = marketName + ': ' + varTitle

    numCategories = len(list(marketdata.values())[0])

    for i in range(numCategories):
        x = []
        y = []
        for key, value in sorted(list(marketdata.items())):
            x.append(key)
            y.append(list(value.values())[i])
        times = list(marketdata.keys())
        times = [toReadableTime(x) for x in times]
        plot = plt.plot(x,y,label=list(value.keys())[i])
#    plot = plt.plot(x,y,label=times[i])
        plt.xlabel('')
        #plt.xlabel([toReadableTime(x) for x in marketdata])
        plt.title(title)
    #plt.xticks(np.arange(0, len(marketdata), 30.0))
#    plt.xticks([toReadableTime(xx) for xx in x])

    if variable != 'risk':
        plt.legend(list(value.keys()))
        plt.legend(bbox_to_anchor=(1.04,0), loc='lower left', ncol=1)

    if tweets:
        times = loadTweetData(tweetDataPath,epochRange)
        for t in times:
            plt.axvline(x=t)

    print(marketdata[1577215619])
    plt.show()


marketID, marketDataPath, tweetDataPath, plotType, epochRange = parseArgs()
tweets = not (tweetDataPath is None)


plot(marketID, plotType,tweets)


