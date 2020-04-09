import numpy as np
import statsmodels.api as sm
from ts_util import forecast_eval,plot
import matplotlib.pyplot as plt


def transform(x):
    #return [[a[0],a[1],a[3],a[4],a[5]] for a in x]
    #return 20 * np.array([[a[2]] for a in x])
    ret = 20 * np.array([a[5] for a in x])
    ret = np.concatenate(([0], ret))
    return np.diff(ret)
# response variable
tweets = [24,47,34,30,39,27,42,    # wed 10/30
        17,18,9,82,21,28,19, # wed 11/6
        49,30,37,25,50,15,43,    # wed 11/13
        35,35,28,16,48,21,18,    # wed 11/20
        9,7,1,1,3,36,34,    # wed 11/27 <-- is off?
        41,16,48,20,105,23,39,    # wed 12/4
        77,123,23,25,27,57,21,        # wed 12/11
        70,73,48,6,9,29,12,     # wed 12/18
        13,35,55,14,3,5,54,    # wed 12/25
        15,5,33,6,2,23,19,    # wed 1/1
        1,33,40,14,29,24,21,    # wed 1/8
        26,25,31,25,8,27,5,    # wed 1/15
        142,29,78,71,37,51,36,    # wed 1/22
        29,44,16,56,34,43,29, # wed 1/29      
        36,15,59,72,54,15,47, # wed 2/5
        17,10,23,45,3,18,37, # wed 2/12
        41,33,47,12,13,39,22,   # wed 2/19
        46,11,24,10,29,49,37,   # wed 2/26
        40,31,25,15,4,35,34,    # 3/4
        24,47,26,24,27,29,47,   # 3/11
        20,13,58,21,82,43,37,   # 3/18
        31,9,32,27,31,15,26]    # 3/25

# test run with last two weeks, starting 3/18
y = [   46,11,24,10,29,49,37,   # wed 2/26
        40,31,25,15,4,35,34,    # 3/4
        24,47,26,24,27,29,47,   # 3/11
        20,13,58,21,82,43,37,   # wed 3/18
        31,9,32,27,31,15,26]    # wed 3/25

x2 = [
    5,4,16,9,1,19,16,
    10,16,24,6,3,16,6,
    10,5,3,2,3,7,6,
    6,8,3,3,2,3,4,
    4,5,4,12,3,5,3]


x = [
    [1,0,1,1,0,0],  # wed 2/26
    [4.5,2,0,0,0,0],
    [7,2,0,3,0,0],
    [1.5,1,0,2,0,0],
    [2,0,0,0,0,0],
    [2,3,0,4,0,0],
    [2,0,1,4,0,0],
    [2.5,2,1,2,1,0],  # wed 3/4
    [4,1,0,4,1,0],
    [1,2,1,4,0,0],
    [2,3,0,0,0,4],
    [2,1,0,0,0,5],
    [2,2,1,3,0,0],
    [3,3,1,0,0,0],
    [3,2,1,2,0,0], # wed 3/11
    [2,2,0,0,0,0],
    [4,1,1,0,0,0],
    [2,0,1,0,0,0],
    [1.5,1,1,0,0,0],
    [1,2,1,0,0,0],
    [1,4,1,0,0,0],  
    [1,4,1,0,0,0],  # wed 3/18
    [2,1,1,2,0,0],
    [0,1,1,0,0,0],
    [2,1,1,0,0,0],
    [2,0,1,0,0,0],
    [2,0,1,0,0,0],
    [3,0,1,0,2,0],
    [2,1,1,0,0,0],  # wed 3/25
    [0,2,1,0,1,0],
    [2,1,1,0,0,0],
    [1,0,0,3,0,0],
    [2,1,1,0,0,0],
    [1.5,1,1,0,1,0],
    [4,1,1,0,0,0]
]

x = transform(x)
#x = x2
plot(x,label='total events')
plot(y,label='tweets')

n = len(y)
test_index = n - 7
x_train = x[:test_index]
y_train = y[:test_index]
x_test = x[test_index:]
y_test = y[test_index:]

mod = sm.OLS(y, x)
res = mod.fit()
print('------ full results ---------')
print(res.summary())

mod = sm.OLS(y_train, x_train)
res = mod.fit()
pred = res.predict(x_test)
print('predicted:')
print(pred)
print('actual:')
print(y_test)

mse, mae = forecast_eval(y_test, pred)
print('mse: ' + str(mse))
print('mae: ' + str(mae))

plt.legend()
plt.show()