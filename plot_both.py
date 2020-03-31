import pandas as pd
import matplotlib.pyplot as plt
from utils import cleanPrint
import numpy as np
import sys

def parseArgs():
    #plot_type = 'tweets'
    if '--type' not in sys.argv:
        return 'tweets'
    return sys.argv[sys.argv.index('--type') + 1]

def plot(df, plotType):

    market = pd.DataFrame(data=df,index=df.index,columns=
        ['239 or fewer','240 - 249','250 - 259','260 - 269',
        '270 - 279','280 - 289','290 - 299','300 - 309','310 or more'])
    
    tweet = pd.DataFrame(data=df,index=df.index,columns=['tweets'])

    if plotType == 'tweets':
        pass 
    if plotType == 'cum':
        tweet = tweet.cumsum()

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    market.plot(ax=ax)
    tweet.plot(ax=ax2,)
    plt.show()



    return 0

plotType = parseArgs()

# read and pre process csv
df = pd.read_csv('abc')
#df = df.set_index('date')
#df = df.drop(['i'],axis=1)
#df = df.drop(['unix'],axis=1)

plot(df, plotType)


# tweet_exp = tweet.ewm(span=600).mean()
# tweet_total = tweet.cumsum()
# pace = tweet_total / 100

# #cleanPrint(market)

# # plot
# fig, ax = plt.subplots()#nrows=2,ncols=1)
# ax2 = ax.twinx()

# market.plot(ax=ax)
# #tweet['tweets'] = tweet['tweets'].astype(np.float)
# #bp = tweet.boxplot(by='tweets')
# #tweet.plot(ax=ax2,)
# #bp.plot()

# #tweet_exp.plot(ax=ax2,color='red',ls='--')
# #tweet_total.plot(ax=ax2,ls='--')

# pace.plot(ax=ax2,ls='--')


# #df.plot(subplots=True,layout=(1,10))
# plt.show()