import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.api as sm
import matplotlib.pyplot as plt

def tweets_to_bins(tweetDataPath, bin_len, start_index=0):
    # read file
    f = open(tweetDataPath, 'r')
    data = f.read()
    data = json.loads(data)
    tweetTimes = []
    for tweet in data:
        # only add if in range of marketdata
        t = int(tweet['timestamp_epochs'])
        tweetTimes.append(t)
    tweetTimes.sort()
    print(tweetTimes)

    # split into bins
    last_time = tweetTimes[-1]
    first_time = tweetTimes[start_index]

    #bin_len = (last_time - first_time) // bins
    bins = (last_time - first_time) // bin_len

    bins_index = 0
    timestamp_index = start_index
    data = []
    while bins_index < bins:
        data.append(0)
        while tweetTimes[timestamp_index] >= bins_index * bin_len + first_time and \
            tweetTimes[timestamp_index] < first_time + (bins_index + 1) * bin_len:
            #print('got here')
            data[bins_index] += 1
            timestamp_index += 1
        bins_index += 1
        

    return data

def process_forecast(fcast,alpha=.05):
    mean = fcast.predicted_mean
    CI = fcast.conf_int(alpha=alpha)
    low_ci = [CI[i][0] for i in range(len(CI))]
    high_ci = [CI[i][1] for i in range(len(CI))]

    return mean, low_ci, high_ci

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
    #return np.concatenate((np.zeros(n//2), ret[n-1:]/n))

def plot_ma(data, k):
    plot(moving_average(data,n=k),label='k=' + str(k))
    

# returns p,q,P,Q with lowest AIC
def grid_search():
    min_aic = 1000000000
    min_vals = (2,2,2,2)
    for p in range(2,5):
        for q in range(2,5):
            for P in range(2,5):
                for Q in range(2,5):
                    try:
                        #print('p,q,P,Q',p,q,P,Q)
                        mod = sm.tsa.statespace.SARIMAX(data, order=(p,0,q), seasonal_order=(P,0,Q,7))
                        res = mod.fit(display=False)
                        #print('aic: ', res.aic)
                        pred = np.array(res.forecast(3))
                        #print(pred)
                        if res.aic < min_aic:
                            min_vals = (p,q,P,Q)
                    except:
                        print('couldnt complete')
    return (p,q,P,Q)

def plot(data,label=''):
    if label is None:
        label = ''
    plt.plot(data,label=label + ' data')

def plot_forecast(data, mean, low_ci, high_ci, label=''):
    if label is None:
        label = ''
    n = len(data)
    mean = np.concatenate((np.zeros(n), mean))

    plt.plot(data, label=label + 'data')
    plt.plot(mean, label=label + 'predicted mean')
    if low_ci is not None:
        low_ci = np.concatenate((np.zeros(n), low_ci))
        plt.plot(low_ci, label=label + 'lower CI')
    if high_ci is not None:
        high_ci = np.concatenate((np.zeros(n), high_ci))
        plt.plot(high_ci, label=label + 'high CI')

def plot_acf(data, label=''):
    sm.graphics.tsa.plot_acf(data, lags=14)

def get_seasonal_components(data, period=7):
    n = len(data)
    days = []
    for i in range(period):
        j = i
        l = []
        while j < n:
            l.append(data[j])
            j += period
        days.append(l)
    return days

# return mean, std, min, max, 25% and 75% quantiles
def get_basic_statistics(data):
    mean = np.mean(data)
    std = np.std(data)
    min_value = min(data)
    max_value = max(data)

    return mean, std, min_value, max_value, np.quantile(data, .25), np.quantile(data, .75)

def seasonal_plot(data,label='',period=7):
    # 7 days
    days = get_seasonal_components(data, period=period)

    # plot seasons
    for i in range(len(days)):
        day = days[i]
        plt.plot(day,label=label+' day ' + str(i))

# given actual and forecasted data, return MSE, MAE
def forecast_eval(actual, predicted):
    assert len(actual) == len(predicted)
    n = len(actual)
    # compute MSE, MAE
    mse = 0
    mae = 0
    n = len(predicted)
    for i in range(n):
        mse += (predicted[i] - actual[i]) ** 2
        mae += abs(predicted[i] - actual[i])
    mse /= n
    mae /= n

    return mse, mae

# evaluates n step forecast, defaults to n = 1
def n_step_forecast_eval(data, test_index, forecast_method, positional_arguments=None,n=1,label=None):
    if label is None:
        label = ''
    N = len(data)
    index = test_index
    mse = 0
    mae = 0
    predicted = []
    count = 0
    while index < N - 1:
        train_data = data[:index]
        if positional_arguments is None:
            mean, _,_ = forecast_method(train_data,n)
        else:
            mean,_,_ = forecast_method(train_data,*positional_arguments)
        se, ae = forecast_eval([data[index + 1]], mean)
        predicted.append(mean[0])
        mse += se
        mae += ae
        index += 1
        count += 1
    mse /= count
    mae /= count
    print('predicted her')
    print(predicted)
    #plot_forecast(data, predicted, None, None, None)
    plt.plot(data,label=label + ' data')
    plt.plot(np.concatenate((np.zeros(test_index), predicted)),label=label + ' predicted')
    return mse, mae