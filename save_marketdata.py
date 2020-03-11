from utils import loadMarketForPlot, parseArgs, thinDF
import sys
import pandas as pd

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

def save_marketdata( marketDataPath,epochRange,marketID, thin, filename):
  marketdata, marketName = loadMarketForPlot('yes', marketDataPath, epochRange, marketID)

  marketdata = pd.DataFrame(marketdata).transpose().sort_index()
  marketdata = thinDF(marketdata,thin)
  marketdata.to_csv(filename,index=False)

marketID, marketDataPath, tweetDataPath, plotType, epochRange, thin, filename = parseArgsLoc()

save_marketdata(marketDataPath, epochRange,marketID, thin, filename)
