import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.api as sm
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import matplotlib.pyplot as plt
from ts_util import tweets_to_bins, plot_acf, plot_forecast, plot, seasonal_plot, process_forecast,n_step_forecast_eval, forecast_eval, plot_ma, get_basic_statistics

p=4
q=4
P=4
Q=4

data = [24,47,34,30,39,27,42,    # wed 10/30
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
        41,33,47,12,13,39,22,
        46,11,24,10,29,49,37,
        40,31,25,15,4,35,34,
        24,47,26,24,27,29,47,
        20,13,58,21,82,43,37,
        31,9,32,27,31,15,26]#,44,33]




def weekly(alpha):
        pred_list = np.zeros(7)
        up_ci = np.zeros(7)
        low_ci = np.zeros(7)


        for i in range(11, 1000,7):
            if i >= len(data) - 2:
                break
            curr_data = data[:i]
            mod = sm.tsa.statespace.SARIMAX(curr_data, order=(p,0,q), seasonal_order=(P,0,Q,7))
            res = mod.fit(disp=False)
            pred = np.array(res.forecast(3))
            
            forecast = res.get_forecast(3)
            CI = forecast.conf_int(alpha=alpha)
            up_ci = np.concatenate((up_ci, np.zeros(4)))
            low_ci = np.concatenate((low_ci, np.zeros(4)))
            up_ci = np.concatenate((up_ci, np.array([CI[0][1],
                CI[1][1], CI[2][1]])))
            low_ci = np.concatenate((low_ci, np.array([CI[0][0],
                CI[1][0],CI[2][0]])))
            
            pred_list = np.concatenate((pred_list, np.zeros(4)))
            pred_list = np.concatenate((pred_list,pred))
            print('week number: ------------', i // 7)
            print('predicted: ', sum(pred))
            print('actual: ', data[i] + data[i+1] + data[i+2])

        plt.plot(data,label="data")
        plt.plot(pred_list,label='predicted')
        plt.plot(up_ci, label='upper ci')
        plt.plot(low_ci, label='lower ci')
        #plt.plot(ci, label='90 percent ci')
        plt.legend()
        plt.show()

# return predicted_mean, low_ci, high_ci for steps ahead of data, with SARIMAX
def sarimax(data, steps, alpha,p,q,P,Q):
        # sarmiax forecast
        mod = sm.tsa.statespace.SARIMAX(data, order=(p,0,q), initialization='approximate_diffuse', seasonal_order=(p,0,q,7))
        res = mod.fit()
        fcast = res.get_forecast(steps)
      
        # get mean and confidence intervals
        mean, low_ci, high_ci = process_forecast(fcast)

        return mean, low_ci, high_ci




# given future forecast, return s (deviation)
def test_forecast(future,predicted):#test_data, train_data):
    assert len(future) == len(predicted)
    s = sum([(future[i] - predicted[i]) ** 2 for i in range(len(future))]) ** .5
    return s


def positive_sarimax(data, steps, alpha,p,q,P,Q):
    data = np.log(data)
    mean, low_ci, high_ci = sarimax(data, steps, alpha, p,q,P,Q)

    mean = np.exp(mean)
    low_ci = np.exp(low_ci)
    high_ci = np.exp(high_ci)

    return mean, low_ci, high_ci

# returns mean, low, high ci for steps forward with simple expoenntial smoothing
def ses(data, steps):
    fit = SimpleExpSmoothing(data).fit()
    fcast = fit.forecast(steps)#.rename(r'$\alpha=%s$'%fit3.model.params['smoothing_level'])

    return fcast, None, None#process_forecast(fcast)

def ses_flat(data, steps):
    fit = SimpleExpSmoothing(data).fit()
    fcast = fit.forecast(steps)

    return fcast[0] * np.ones(steps), None, None

def naive_mean(data, steps):
    return np.mean(data)*np.ones(steps), None, None

def bouncy_forecast(data, steps, thresh=.25):
    assert steps == 1
    ql = np.quantile(data, thresh)
    qh = np.quantile(data, 1 - thresh)
    mean = np.mean(data)

    if data[-1] > qh:
        return [ql], None, None
    if data[-1] < ql:
        return [qh], None, None
    return [mean], None, None

n = len(data)
train_data = data[:n - 10]
test_data = data[n - 10:]

#mean, low, high = sarimax(train_data,10, .05,p,q,P,Q)
#plot_forecast(data, mean, low,high,label='ses')

#mean, low, high = sarimax(data,10,.05,p,q,P,Q)
#plot_forecast(data, mean, low,high,label='sarimax')
#plot_acf(data)
#seasonal_plot(data)

# steps = 1
test_index = len(data) - 14
#mse, mae = n_step_forecast_eval(data, test_index, sarimax, (1, .05, p,q,P,Q),label='sarimax')
#print('mse sarimax: ' + str(mse))
#print('mae sarmimax: ' + str(mae))

# mse, mae = n_step_forecast_eval(data, test_index, ses,label='ses')
# print('mse ses: ' + str(mse))
# print('mae ses: ' + str(mae))

# mse, mae = n_step_forecast_eval(data, test_index, naive_mean,label='naive')
# print('mse naive: ' + str(mse))
# print('mae naive: ' + str(mae))

# mse, mae = n_step_forecast_eval(data, test_index, bouncy_forecast,(1,.1),label='bouncy')
# print('mse bouncy: ' + str(mse))
# print('mae bouncy: ' + str(mae))


plot(np.diff(data))

#plot_ma(data, 9)
#plot_ma(data, 15)
#plot_ma(data, 25)



plt.legend()
plt.show()
