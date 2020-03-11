import os
import json
from datetime import datetime
from time import mktime as mktime
import sys
import pandas as pd
import numpy as np

def thinDF(df, n):
  return df[np.mod(np.arange(df.index.size),n) == 0]

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

def marketFromID(data, marketID):
    markets = data['markets']
    for m in markets:
        if str(m['id']) == str(marketID):
            return m
    print('error: could not find market with id ' + str(marketID))
    return None

def toReadableTime(unixtime):
    ts = int(unixtime)

    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def dateToUnix(date):
#    return time.mktime(datetime.strptime(date,'%m/%d/%Y').timetuple())
    return int(mktime(datetime.strptime(date,'%Y-%m-%d %H:%M:%S').timetuple()))


# in epoch range for plotting?
def inRange(t, epochRange):
    if epochRange is None:
        return True
    return t > epochRange[0] and t < epochRange[1]


def loadTweetData(tweetDataPath,epochRange):

    # load tweet data
    f = open(tweetDataPath, 'r')
    data = f.read()
    data = json.loads(data)
    tweetTimes = []
    for tweet in data:
        # only add if in range of marketdata
        t = int(tweet['timestamp_epochs'])
        if inRange(t,epochRange):
            tweetTimes.append(int(tweet['timestamp_epochs']))
    tweetTimes.sort()

    return tweetTimes


def loadMarketForPlot(variable,marketDataPath,epochRange,marketID):
    marketdata = dict()
    market = 'hi'
    foundMarket = False
    for filename in os.listdir(marketDataPath):
        #print('here')
        if not filename.isnumeric():
          #print(filename)
          continue
        key = int(filename)
        #print('key is ' + str(key))
        if inRange(key,epochRange):
            #print('123')
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
                foundMarket = True
                found = True
                break
        if not found:
            print('couldnt find market with market id ' + marketID)
#            break
            continue
        contracts = market['contracts']
        prices = dict()
        for contract in contracts:
            if variable == 'yes':
                prices[contract['name']] = contract['bestBuyYesCost']
            if variable == 'no':
                prices[contract['name']] = contract['bestBuyNoCost']
            if variable == 'risk':
                prices[contract['name']] = risk(market)
        marketdata[key] = prices
    if not foundMarket:
      print('couldnt find market')
    #print(marketdata)
    #print(market['name'])
    return marketdata, market['name']


