import numpy as np
import matplotlib.pyplot as plt
import copy
import random

res = 15

rdt = [24,47,34,30,39,27,42,    # wed 10/30
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
        31,9,32,27,31,15,26,#]#,
        5,19,11,70,23,24,14,    # wed 4/1
        21,10,78]# wed 4/8



potus = [
    25,4
]

# sample an element from data with probabilities
# given by probability vector p
def sample(data, p):
    assert len(data) == len(p)
    i = len(p) - 1
    #print(p)
    u = np.random.random()
    while u > p[i]:
        i -= 1
    return data[i]

# generates exponentially decaying probability distribution
# according to shape parameter alpha
# (for decaying probabilities use negative indexing)
# n is the length of data / length of distribution
def exp_decay_generator(n, alpha=.5):
    c = sum([np.exp(-(alpha * i)) for i in range(1, n+1)])
    p = []
    for i in range(1, n + 1):
        p.insert(0, sum([np.exp(-(alpha * j)) for j in range(1,i + 1)]) / c)
    
    return p

def uniform_generator(n):
    ret = (1 / n) * np.ones(n)
    ret = np.cumsum(ret)
    return np.flip(ret)


# simulates n steps ahead of data
# generates one step at a time according prob. dist generated
# by distributions in dists
def n_step_sim(data, n, dists):
    temp_data = copy.copy(data)
    pred = []
    
    for i in range(n):
        p = dists[i]
        predicted = sample(temp_data, p)
        temp_data.append(predicted)
        pred.append(predicted)
        #print(predicted)
    return pred

# given list of len 8 which gives the lower bound for brackets 2 - 9, return
# appropriate bins object for numpy.hist
def bins_from_bracket_list(bracket_list):
    ret = np.array(bracket_list)
    ret = np.insert(ret, 0, 0)
    ret = np.append(ret, 1000)
    return ret

# return the empircal probability distribution of number of tweets
# in the next n days, with tweet counts (hist endpoints) given in bins
# dist generator gives generation of distributions
def emperical_probability_dist(data, n, dist_generator, positional_arguments, bins, iters = 1000):
    counts = []
    dists = []
    for i in range(n):
        if positional_arguments is None:
            dists.append(dist_generator(len(data) + i))
        else:
            dists.append(dist_generator(len(data) + i, positional_arguments))
    for _ in range(iters):
        #counts += n_step_sim(data, n, len(data), alpha=alpha)
        counts.append(sum(n_step_sim(data, n, dists)))
    hist,_ = np.histogram(counts, bins = bins)
    return hist / iters, np.array(counts)


def eval_sim(data,test_index,steps, alpha,iters=10000,bins=[100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280]):
    
    n = len(data)
    histograms = []
    counts = []
    for i in range(test_index, n - steps, steps):
        weekly_counts = []
        for _ in range(iters):
            #pred = n_step_sim(data[:i], steps, len(data[:i]), alpha=alpha)
            #pred = n_step_sim_equal_weights(data[:i], steps, len(data[:i]))
            pred = n_step_sim_gaussian(data[:i], steps, len(data[:i]), alpha=alpha)
            weekly_counts.append(sum(pred))
        # partition into bins
        hist, _ = np.histogram(weekly_counts,bins=bins)
        hist = np.array(hist, dtype=float)
        hist /= iters
        counts.append(weekly_counts)
        histograms.append(hist)

    return histograms, counts

# compares market prices to predicted probabilites at t0 + 24hrs, t0 + 48hrs, ..., t0 + 6 days
def eval_week(data, test_index, market_prices, bracket_list,alpha,iters=1000):
    num_checkpoints = 6
    assert len(market_prices) == num_checkpoints
    predicted = []
    market = []
    bins = bins_from_bracket_list(bracket_list)

    for i in range(num_checkpoints):
        # compute emperical dist
        curr_data = data[:test_index + i]
        bins = [b - data[test_index + i ] for b in bins]
        print(bins)
        predicted_dist = emperical_probability_dist(curr_data, num_checkpoints - i, alpha=alpha,bins=bins,iters=iters)
        market_dist = market_prices[i]
        predicted.append(predicted_dist)
        market.append(market_dist)

    return predicted, market


# plt.axvline(x=sum(tweets[17 + 21:21 + 21]), color = 'r')

# evaluate week of 2/12
bracket_list = [240,250,260,270,280,290,300,310]
market_prices = []
market_prices.append([.42,.12,.1,.09,.09,.08,.08,.07,.14])
market_prices.append([.66,.12,.09,.06,.05,.04,.04,.03,.08])
market_prices.append([.8,.07,.05,.05,.04,.04,.04,.04,.04])
market_prices.append([.83,.08,.06,.04,.03,.02,.02,.01,.03])
market_prices.append([.92,.05,.03,.02,.01,.01,.01,.01,.01])
market_prices.append([.97,.04,.02,.01,.01,.01,.01,.01,.01])

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
        17,10,23,45,3,18,37]

test_index = len(data) - 7

#predicted, market = eval_week(data, test_index, market_prices, bracket_list, .4,iters=10)

# evaluate week of 1/ 15
bracket_list = [150,160,170,180,190,200,210,220]
market_prices = []
market_prices.append([.28,.11,.11,.10,.10,.07,.07,.07,.26])
market_prices.append([.66,.12,.09,.06,.05,.04,.04,.03,.08])
market_prices.append([.8,.07,.05,.05,.04,.04,.04,.04,.04])
market_prices.append([.83,.08,.06,.04,.03,.02,.02,.01,.03])
market_prices.append([.92,.05,.03,.02,.01,.01,.01,.01,.01])
market_prices.append([.97,.04,.02,.01,.01,.01,.01,.01,.01])

# data = [24,47,34,30,39,27,42,    # wed 10/30
#         17,18,9,82,21,28,19, # wed 11/6
#         49,30,37,25,50,15,43,    # wed 11/13
#         35,35,28,16,48,21,18,    # wed 11/20
#         9,7,1,1,3,36,34,    # wed 11/27 <-- is off?
#         41,16,48,20,105,23,39,    # wed 12/4
#         77,123,23,25,27,57,21,        # wed 12/11
#         70,73,48,6,9,29,12,     # wed 12/18
#         13,35,55,14,3,5,54,    # wed 12/25
#         15,5,33,6,2,23,19,    # wed 1/1
#         1,33,40,14,29,24,21,    # wed 1/8
#         26,25,31,25,8,27,5] # wed 1/15
# test_index = len(data) -7

# predicted, market = eval_week(data, test_index, market_prices, bracket_list, .05,iters=1000)


#bracket_list = [140,150,160,170,180,190,200,210]
# alpha = 1
# iters = 10000
# n = 5
# bins = bins_from_bracket_list(bracket_list)
# bins = [b - (21+10+78) for b in bins]

# for alpha in [.03,.05,.07,.09,.11,.13,.15]:
#     pred = emperical_probability_dist(rdt,n,exp_decay_generator,(alpha),bins=bins,iters=iters)
#     #pred = emperical_probability_dist(rdt,n,uniform_generator,None,bins=bins,iters=iters)
#     print('predicted distribution, for n=' + str(n) + ' steps forward and alpha=' + str(alpha) + ':')
#     print(pred)

# #plt.hist(pred)
# plt.show()

