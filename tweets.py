from utils import tweetToPandas, loadMarketForPlot, thinDF, loadTweetData
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

WEEKLEN = 604800

#epochRange = [1582131600, 1582736400]
epochRange = [1582231600, 1582636400]
# tweet
df = tweetToPandas('twitterdata/realdonaldtrump-1583963222', epochRange,60)
#df.plot()
tweetTimes = loadTweetData('twitterdata/realdonaldtrump-1583963222',epochRange)
df_exp = df.ewm(span=100).mean()

def f(row):
    #unix_time = pd.to_datetime(row['unix']).astype(int) / 10**9
    unix_time = row['unix']
    count = 0
    for time in tweetTimes:
        if time > unix_time - 60 and time < unix_time:
            count += 1
    return count

def f2(row):
    unix_time = row['unix']
    return row['cum_tweets'] * WEEKLEN / (unix_time - epochRange[0])

market_df = pd.read_csv('feb19')

market_df['tweet_count'] = market_df.apply(f,axis=1)

# cumulative tweets
init = 0
x_diff = market_df['tweet_count'].tail(-1)
market_df['cum_tweets'] = np.r_[init, x_diff].cumsum().astype(int)

new_df = market_df.join(df_exp)
new_df['tweet_count'] = new_df['tweet_count'].ewm(span=200).mean()
new_df['cum_tweets'] = new_df['cum_tweets']
new_df['pace'] = new_df.apply(f2, axis=1) / 200
new_df['cum_tweets'] /= 50

new_df['unix'] = pd.to_datetime(new_df['unix'],unit='s')
new_df = new_df.set_index('unix')



#exponential smooth count


new_df.plot()

#market_df.plot()

plt.show()