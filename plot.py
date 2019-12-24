import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time

def getMarketDataRange(marketdata):
    minimum = 100000000000
    maximum = 0
    for key in marketdata:
        if key < minimum:
            minimum = key
        if key > maximum:
            maximum = key
    print(minimum,maximum)
    return minimum, maximum

def tweetTimes():
    f = open('yang_tweets.json', 'r')
    data = f.read()
    data = json.loads(data)
    minimum, maximum = getMarketDataRange(marketdata)
    timestamps = []
    for tweet in data:
        # only add if in range of marketdata
        t = int(tweet['timestamp_epochs'])
        if t > minimum and t < maximum:
            # correct for utc to current timezone
            timestamps.append(int(tweet['timestamp_epochs']))
    timestamps.sort()
    return timestamps


def dateToUnix(date):
    return time.mktime(datetime.strptime(date,'%m/%d/%Y').timetuple())

def toReadableTime(unixtime):
    ts = int(unixtime)

    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def addToDict(filename):
    f = open(path + filename, 'r')
    data = f.read()
    data = json.loads(data)
    marketdata[int(filename)] = data

def loadData(minimum=None, maximum=None):
    # populate marketdata dictionary
    if not (minimum is None and maximum is None):
        minimum = int(minimum)
        maximum = int(maximum)
    for filename in os.listdir(path):
        s = int(filename)
        if (minimum is None and maximum is None) or (s > minimum and s < maximum):
            addToDict(filename)
    #marketdata = {int(k) : v for k, v in marketdata.items()}

def risk(market):
    risk = 0
    for contract in market['contracts']:
        if contract['bestBuyNoCost'] is None:
            continue
        risk += 1 - float(contract['bestBuyNoCost'])
    risk *= 100
    return risk

def plot(marketdata, marketID, variable, tweets=True):
    # plot market with marketID
    marketPrices = dict()
    if len(marketdata) < 1:
        print('no marketdata to plot')
        return
    for key in marketdata:
        # find market with marketID
        timex = marketdata[key]
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
        plt.xlabel([toReadableTime(x) for x in marketPrices])
        plt.title(title)
    #plt.xticks(np.arange(0, len(marketPrices), 30.0))

    if variable != 'risk':
        plt.legend(list(value.keys()))
        plt.legend(bbox_to_anchor=(1.04,0), loc='lower left', ncol=1)

    if tweets:
        times = tweetTimes()
        for t in times:
            plt.axvline(x=t)
#    plt.axvline(x=1577030956)

    plt.show()

def praseArgs():


marketID = sys.argv[1]
variable = sys.argv[2]
marketdata = dict()
path = 'marketdata/'
numArgs = len(sys.argv) - 1

if numArgs > 2:
    loadData(dateToUnix(sys.argv[3]), dateToUnix(sys.argv[4]))
else:
    loadData()

plot(marketdata, marketID, variable)


