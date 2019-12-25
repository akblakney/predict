import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time

def dateToUnix(date):
    return time.mktime(datetime.strptime(date,'%m/%d/%Y').timetuple())

def toReadableTime(unixtime):
    ts = int(unixtime)

    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# in epoch range for plotting?
def inRange(t):
    if epochRange is None:
        return True
    return t > epochRange[0] and t < epochRange[1]

def loadData(tweets, minimum=None, maximum=None):

    # load tweet data
    f = open(tweetDataPath, 'r')
    data = f.read()
    data = json.loads(data)
    tweetTimes = []
    for tweet in data:
        # only add if in range of marketdata
        t = int(tweet['timestamp_epochs'])
        if inRange(t):
            tweetTimes.append(int(tweet['timestamp_epochs']))
    tweetTimes.sort()

    return tweetTimes

def risk(market):
    risk = 0
    for contract in market['contracts']:
        if contract['bestBuyNoCost'] is None:
            continue
        risk += 1 - float(contract['bestBuyNoCost'])
    risk *= 100
    return risk

def plot(marketID, variable, tweets):
    marketPrices = dict()
    for filename in os.listdir(marketDataPath):
        t = int(filename)
        key = t
        if inRange(t):
            f = open(marketDataPath + filename, 'r')
            data = f.read()
            data = json.loads(data)
        else:
            continue
        timex = data
        markets = timex['markets']
        market = 'hi'
        found = False
        for m in markets:
            if str(m['id']) == str(marketID):
                market = m
                found = True
                break
        if not found:
            print('couldnt find market with market id ' + marketID)
            break
        contracts = market['contracts']
        prices = dict()
        for contract in contracts:
            if variable == 'yes':
                prices[contract['name']] = contract['bestBuyYesCost']
            if variable == 'no':
                prices[contract['name']] = contract['bestBuyNoCost']
            if variable == 'risk':
                prices[contract['name']] = risk(market)
        marketPrices[key] = prices

    if variable == 'yes':
        varTitle = 'yes prices'
    if variable == 'no':
        varTitle = 'no prices'
    if variable == 'risk':
        varTitle = 'market risk'
    title = market['name'] + ': ' + varTitle
    marketPrices = {int(k) : v for k, v in marketPrices.items()}

    numCategories = len(list(marketPrices.values())[0])

    for i in range(numCategories):
        x = []
        y = []
        for key, value in sorted(list(marketPrices.items())):
            x.append(key)
            y.append(list(value.values())[i])
        times = list(marketPrices.keys())
        times = [toReadableTime(x) for x in times]
        plot = plt.plot(x,y,label=list(value.keys())[i])
#    plot = plt.plot(x,y,label=times[i])
        plt.xlabel('')
        #plt.xlabel([toReadableTime(x) for x in marketPrices])
        plt.title(title)
    #plt.xticks(np.arange(0, len(marketPrices), 30.0))
#    plt.xticks([toReadableTime(xx) for xx in x])

    if variable != 'risk':
        plt.legend(list(value.keys()))
        plt.legend(bbox_to_anchor=(1.04,0), loc='lower left', ncol=1)

    if tweets:
        times = tweetTimes
        for t in times:
            plt.axvline(x=t)

    plt.show()

def parseArgs():
    # id
    if '--id' in sys.argv:
        marketID = sys.argv[sys.argv.index('--id') + 1]
    else:
        print('error: no market id specified')
        sys.exit()

    # marketdata
    if '--marketdata' in sys.argv:
        marketDataPath = sys.argv[sys.argv.index('--marketdata') + 1]
        # add / to end of directory if not there
        if marketDataPath[-1] != '/':
            marketDataPath.append('/')
    else:
        marketDataPath = 'marketdata/'

    # tweetdata
    if '--tweetdata' in sys.argv:
        tweetDataPath = sys.argv[sys.argv.index('--tweetdata') + 1]
    else:
        tweetDataPath = None

    # plot-type
    if '--plot-type' in sys.argv:
        plotType = sys.argv[sys.argv.index('--plot-type') + 1]
    else:
        plotType = 'yes'

    # epoch-range
    if '--epoch-range' in sys.argv:
        epochRange = sys.argv[sys.argv.index('--epoch-range') + 1].split('-')
        epochRange = [int(x) for x in epochRange]
    else:
        epochRange = None

    return marketID, marketDataPath, tweetDataPath, plotType, epochRange


marketID, marketDataPath, tweetDataPath, plotType, epochRange = parseArgs()
tweets = not (tweetDataPath is None)

if epochRange is not None:
    tweetTimes = loadData(tweets, epochRange[0], epochRange[1])
else:
    tweetTimes = loadData(tweets)

plot(marketID, plotType,tweets)


