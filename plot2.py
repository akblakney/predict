import pandas as pd
import sys
import matplotlib.pyplot as plt
from utils import thinDF

def probOfIncrease(arr):
  for i in range(arr.size):
    future = arr.tail(-(i))
    max_future = future.max()
    if max_future > arr.iloc[i]:
      arr.iloc[i] = 1
    else:
      arr.iloc[i] = 0
  return arr

def propOfGreater(arr):
  for i in range(arr.size):
    future = arr.tail(arr.size-i)
    count = 0
    for j in range(i + 1, arr.size):
      if arr.iloc[j] > arr.iloc[i]:
        count += 1
    arr.iloc[i] = count / (arr.size - i)

  return arr

def try2(arr):
  l = arr.values.tolist()
  for i in range(len(l)):
    future = l[-(len(l) - i):]
    if max(future) > l[i]:
      l[i] = 1
    else:
      l[i] = 0
  return pd.Series((v for v in l))

def try3(arr):
  l = arr.values.tolist()
  for i in range(len(l)):
    count = 0
    for j in range(i + 1, len(l)):
      if l[j] > l[i]:
        count += 1
    l[i] = count / (len(l) - i)

  return pd.Series((v for v in l))
def plot(dfFilename):
  # pre-process
  df = pd.read_csv(dfFilename)
#  df = thinDF(df, 9)

  # plot original
  df.plot()

  # plot prob of increase
#  inc = df.copy()
#  inc = inc.apply(try2,axis=0)
#  df = df.apply(propOfGreater,axis=0)
#  inc.plot()

  # plot differenced
#  df = df.diff()
#  df.plot()
#  plt.title('Jan. 8 to Jan. 15')


  # pct change
  df = df.rolling(window=60).sum()
  #df.plot()
  df = df.apply(try3,axis=0)
  #df.plot()
  df = df.rolling(window=20).sum()
  df.plot()
  plt.show()  

def parseArgsLoc():
  # id
#  if '--id' in sys.argv:
#    marketID = sys.argv[sys.argv.index('--id') + 1]
#  else:
#    print('error: no market id specified')
#    sys.exit()

#  variable = 'yes'

  if '--filename' not in sys.argv:
    print('error: no filename given for dataframe')
    sys.exit()
  filename = sys.argv[sys.argv.index('--filename') + 1]

  return filename

dfFilename = parseArgsLoc()
plot(dfFilename)
