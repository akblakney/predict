from utils import loadMarketForPlot, parseArgs, thinDF, loadTweetData, cleanPrint
import sys
import pandas as pd
from bisect import bisect_right, bisect_left

def parseArgsLoc():
  marketID, marketDataPath, tweetDataPath, plotType, epochRange = parseArgs()
  
  # thin
  thin = 1
  if '--thin' in sys.argv:
    thin = int(sys.argv[sys.argv.index('--thin') + 1])

  # filename
  if '--filename' not in sys.argv:
    print('must give filename to save to')
    sys.exit()

  filename = sys.argv[sys.argv.index('--filename') + 1]

  return marketID, marketDataPath, tweetDataPath, plotType, epochRange, thin, filename



def save_marketdata( marketDataPath,epochRange,marketID, thin, filename, tweetDataPath):
  marketdata, marketName = loadMarketForPlot('yes', marketDataPath, epochRange, marketID)

  marketdata = pd.DataFrame(marketdata).transpose().sort_index()
  marketdata = thinDF(marketdata,thin)
  print('before tweets')
  cleanPrint(marketdata)
  # add tweets
  if tweetDataPath is not None:
    marketdata = add_tweets(tweetDataPath, marketdata)

  print('after tweets')
  cleanPrint(marketdata)
  
  marketdata['date'] = pd.to_datetime(marketdata['unix'],unit='s')
  marketdata.index.name = 'i'
  marketdata.to_csv(filename)#,index=False)

def f(row, interval,tweetTimes):
  unix_time = row['unix']
  print('a')
  print(unix_time - interval)
  # start_index = tweetTimes.index(tweetTimes[bisect_right(tweetTimes, unix_time - interval)])
  # end_index = tweetTimes.index(tweetTimes[bisect_left(tweetTimes, unix_time)])
  start_index = bisect_right(tweetTimes, unix_time - interval)
  end_index = bisect_left(tweetTimes, unix_time)
  return end_index - start_index


# add tweet data to df
def add_tweets(tweetDataPath, df):
  tweetTimes = sorted(loadTweetData(tweetDataPath, epochRange))
  #df = df.rename_axis('unix')
  df['unix'] = df.index
  print('hhh')
  print(len(tweetTimes))
  interval = df['unix'].iloc[1] - df['unix'].iloc[0]

  df['tweets'] = df.apply(f, axis=1,args=(interval,tweetTimes))

  return df


marketID, marketDataPath, tweetDataPath, plotType, epochRange, thin, filename = parseArgsLoc()
save_marketdata(marketDataPath, epochRange,marketID, thin, filename, tweetDataPath)
