import pandas as pd
import matplotlib.pyplot as plt
from utils import cleanPrint
import numpy as np

# read and pre process csv
df = pd.read_csv('abc')
df = df.set_index('date')
df = df.drop(['i'],axis=1)
df = df.drop(['unix'],axis=1)

market_df = pd.DataFrame(data=df,index=df.index,columns=
    ['239 or fewer','240 - 249','250 - 259','260 - 269',
    '270 - 279','280 - 289','290 - 299','300 - 309','310 or more'])
tweet_df = pd.DataFrame(data=df,index=df.index,columns=['tweets'])

#cleanPrint(market_df)

# plot
fig, ax = plt.subplots()#nrows=2,ncols=1)
ax2 = ax.twinx()

market_df.plot(ax=ax)
#tweet_df['tweets'] = tweet_df['tweets'].astype(np.float)
#bp = tweet_df.boxplot(by='tweets')
tweet_df.plot(ax=ax2,marker='.')
#bp.plot()



#df.plot(subplots=True,layout=(1,10))
plt.show()