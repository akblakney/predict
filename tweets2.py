import pandas as pd
import matplotlib.pyplot as plt
# read csv
df = pd.read_csv('abc')
df = df.set_index('date')
df = df.drop(['i'],axis=1)
df = df.drop(['unix'],axis=1)

#
df.plot()
plt.show()